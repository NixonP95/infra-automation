import os
import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# -----------------------------
# Configuration & Credentials
# -----------------------------
# Preferred: let the SDK resolve credentials automatically (instance profile / SSO / profile).
# If env creds are present, boto3.Session below will use them.
REGION = (
    os.getenv("AWS_DEFAULT_REGION")
    or os.getenv("AWS_REGION")
    or os.getenv("REGION")
    or "us-east-2"
)

AWS_PROFILE = os.getenv("AWS_PROFILE")  # optional

# Optional filters
FILTER_TAG_KEY = os.getenv("FILTER_TAG_KEY")       # e.g., "Environment"
FILTER_TAG_VALUE = os.getenv("FILTER_TAG_VALUE")   # e.g., "prod"
FILTER_VPC_ID = os.getenv("FILTER_VPC_ID")         # e.g., "vpc-0123456789abcdef0"

# Botocore client config (retries, timeouts)
boto_cfg = Config(
    region_name=REGION,
    retries={"max_attempts": 10, "mode": "standard"},
    read_timeout=20,
    connect_timeout=5,
)

# Create a Session that respects:
# - EC2 instance profile / SSO / shared config
# - or env vars (AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_SESSION_TOKEN)
# - or a specific AWS_PROFILE if provided
try:
    if AWS_PROFILE:
        session = boto3.Session(profile_name=AWS_PROFILE, region_name=REGION)
    else:
        session = boto3.Session(region_name=REGION)

    ec2_client = session.client("ec2", config=boto_cfg)
    elb_client = session.client("elbv2", config=boto_cfg)
except Exception as e:
    # Fail fast with a readable error if creds/region are broken
    raise RuntimeError(f"Failed to initialize AWS clients: {e}") from e


# -----------------------------
# Helpers
# -----------------------------
def paginate(method, result_key: str, **kwargs):
    """
    Generic paginator helper.
    method: a bound boto3 client method (e.g., ec2_client.describe_instances)
    result_key: the top-level key with the list (e.g., 'Reservations', 'LoadBalancers', 'Images', 'Vpcs')
    kwargs: API-specific params
    """
    items = []
    next_token_key = "NextToken"
    token_param = "NextToken"

    while True:
        resp = method(**({**kwargs, **({token_param: kwargs.get(token_param)} if kwargs.get(token_param) else {})}))
        items.extend(resp.get(result_key, []))
        next_token = resp.get(next_token_key) or resp.get("NextMarker") or resp.get("NextToken")
        if not next_token:
            break
        kwargs[token_param] = next_token
    return items


def get_instances():
    """Return a flat list of EC2 instances with optional filters."""
    filters = []

    if FILTER_VPC_ID:
        filters.append({"Name": "vpc-id", "Values": [FILTER_VPC_ID]})

    if FILTER_TAG_KEY and FILTER_TAG_VALUE:
        filters.append({"Name": f"tag:{FILTER_TAG_KEY}", "Values": [FILTER_TAG_VALUE]})

    kwargs = {}
    if filters:
        kwargs["Filters"] = filters

    reservations = paginate(ec2_client.describe_instances, "Reservations", **kwargs)
    instances = []
    for r in reservations:
        for i in r.get("Instances", []):
            instances.append(i)
    return instances


def get_vpcs():
    return paginate(ec2_client.describe_vpcs, "Vpcs")


def get_load_balancers():
    # elbv2 uses 'NextMarker' for pagination, but our paginate helper handles it
    return paginate(elb_client.describe_load_balancers, "LoadBalancers")


def get_account_amis():
    # Only images owned by the account
    return paginate(ec2_client.describe_images, "Images", Owners=["self"])


def safe_get_public_ip(instance):
    return instance.get("PublicIpAddress") or "N/A"


# -----------------------------
# Routes
# -----------------------------
@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"}), 200


@app.route("/")
def home():
    try:
        instances = get_instances()
        vpcs = get_vpcs()
        lbs = get_load_balancers()
        amis = get_account_amis()

        instance_data = []
        for inst in instances:
            # Derive Name tag if present
            name_tag = next((t["Value"] for t in inst.get("Tags", []) if t.get("Key") == "Name"), "N/A")

            # Security group names/ids
            sgs = []
            for sg in inst.get("SecurityGroups", []):
                sgs.append(f"{sg.get('GroupName','')} ({sg.get('GroupId','')})")
            sg_str = ", ".join(sgs) if sgs else "N/A"

            subnet_id = inst.get("SubnetId", "N/A")

            instance_data.append({
                "ID": inst.get("InstanceId", "N/A"),
                "Name": name_tag,
                "State": inst.get("State", {}).get("Name", "unknown"),
                "Type": inst.get("InstanceType", "N/A"),
                "AZ": inst.get("Placement", {}).get("AvailabilityZone", "N/A"),
                "Public IP": safe_get_public_ip(inst),
                "Private IP": inst.get("PrivateIpAddress", "N/A"),
                "Security Groups": sg_str,
                "Subnet": subnet_id,
            })

        vpc_data = [{"VPC ID": v.get("VpcId", "N/A"), "CIDR": v.get("CidrBlock", "N/A")} for v in vpcs]
        lb_data = [{"LB Name": lb.get("LoadBalancerName", "N/A"), "DNS Name": lb.get("DNSName", "N/A"), "Type": lb.get("Type", "N/A")} for lb in lbs]
        ami_data = [{"AMI ID": ami.get("ImageId", "N/A"), "Name": ami.get("Name", "N/A")} for ami in amis]

        html_template = """
        <html>
        <head>
            <title>AWS Resources</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 24px; }
                h1 { margin-top: 32px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
                th { background: #f6f6f6; }
                code { background: #f2f2f2; padding: 2px 4px; border-radius: 4px; }
            </style>
        </head>
        <body>
            <h1>Running EC2 Instances</h1>
            <table>
                <tr>
                    <th>ID</th><th>Name</th><th>State</th><th>Type</th><th>AZ</th>
                    <th>Public IP</th><th>Private IP</th><th>Security Groups</th><th>Subnet</th>
                </tr>
                {% for instance in instance_data %}
                <tr>
                    <td>{{ instance['ID'] }}</td>
                    <td>{{ instance['Name'] }}</td>
                    <td>{{ instance['State'] }}</td>
                    <td>{{ instance['Type'] }}</td>
                    <td>{{ instance['AZ'] }}</td>
                    <td>{{ instance['Public IP'] }}</td>
                    <td>{{ instance['Private IP'] }}</td>
                    <td>{{ instance['Security Groups'] }}</td>
                    <td>{{ instance['Subnet'] }}</td>
                </tr>
                {% endfor %}
            </table>

            <h1>VPCs</h1>
            <table>
                <tr><th>VPC ID</th><th>CIDR</th></tr>
                {% for vpc in vpc_data %}
                <tr><td>{{ vpc['VPC ID'] }}</td><td>{{ vpc['CIDR'] }}</td></tr>
                {% endfor %}
            </table>

            <h1>Load Balancers</h1>
            <table>
                <tr><th>LB Name</th><th>DNS Name</th><th>Type</th></tr>
                {% for lb in lb_data %}
                <tr><td>{{ lb['LB Name'] }}</td><td>{{ lb['DNS Name'] }}</td><td>{{ lb['Type'] }}</td></tr>
                {% endfor %}
            </table>

            <h1>Available AMIs (Owned by this Account)</h1>
            <table>
                <tr><th>AMI ID</th><th>Name</th></tr>
                {% for ami in ami_data %}
                <tr><td>{{ ami['AMI ID'] }}</td><td>{{ ami['Name'] }}</td></tr>
                {% endfor %}
            </table>

            <p>Region: <code>{{ region }}</code></p>
            {% if tag_key and tag_value %}
                <p>Filters: tag <code>{{ tag_key }}</code>=<code>{{ tag_value }}</code></p>
            {% endif %}
            {% if vpc_filter %}
                <p>Filter VPC: <code>{{ vpc_filter }}</code></p>
            {% endif %}
        </body>
        </html>
        """

        return render_template_string(
            html_template,
            instance_data=instance_data,
            vpc_data=vpc_data,
            lb_data=lb_data,
            ami_data=ami_data,
            region=REGION,
            tag_key=FILTER_TAG_KEY,
            tag_value=FILTER_TAG_VALUE,
            vpc_filter=FILTER_VPC_ID,
        )

    except (ClientError, BotoCoreError) as e:
        # Render a readable error page without leaking secrets
        return f"<h1>Error talking to AWS</h1><pre>{str(e)}</pre>", 500
    except Exception as e:
        return f"<h1>Unexpected error</h1><pre>{str(e)}</pre>", 500


if __name__ == "__main__":
    # Flask on 0.0.0.0:5001 (match your SG rule)
    app.run(host="0.0.0.0", port=5001, debug=True)
