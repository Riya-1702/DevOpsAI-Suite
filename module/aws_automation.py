def run():
    import streamlit as st
    import boto3
    from botocore.exceptions import ClientError

    # --- AWS Configuration (IMPORTANT: Best practice is to use IAM Roles) ---
    # If running on an EC2 instance with an appropriate IAM Role,
    # Boto3 will automatically pick up credentials.
    # For local testing, you might use credentials from environment variables
    # or ~/.aws/credentials. NEVER hardcode them here for production.
    #
    # Initialize EC2 client (Boto3 will look for credentials in standard locations:
    # IAM Role, environment variables, ~/.aws/credentials)
    ec2 = boto3.client('ec2')



    st.title("🚀 EC2 Instance Manager")
    st.write("Launch and terminate Amazon EC2 instances directly from this app.")

    # --- Section for Launching Instances ---
    st.header("Launch New Instance")

    instance_name = st.text_input("Instance Name Tag", "MyStreamlitInstance", key="launch_name")
    instance_type = st.selectbox(
        "Instance Type",
        [
            "t2.micro", "t2.small", "t2.medium",
            "t3.micro", "t3.small", "t3.medium",
            "m5.large", "m5.xlarge"
        ],
        index=0, # Default to t2.micro
        key="launch_type"
    )

    # You'll need to find a suitable AMI ID for your region.
    # This is a common Amazon Linux 2 AMI ID for us-east-1 (N. Virginia).
    # Always verify the correct AMI ID for your chosen region and OS.
    ami_id = st.text_input(
        "AMI ID (Amazon Machine Image)",
        "ami-053b0c53444070a2b", # Example: Amazon Linux 2 AMI in us-east-1
        key="launch_ami"
    )

    key_pair_name = st.text_input("Key Pair Name (for SSH access)", "", key="launch_keypair")
    st.info("Ensure this Key Pair exists in your AWS account and region.")

    security_group_ids_input_launch = st.text_input(
        "Security Group IDs (comma-separated)",
        "sg-xxxxxxxxxxxxxxxxx", # Replace with your actual Security Group ID
        key="launch_sg_ids"
    )
    st.info("Separate multiple IDs with a comma (e.g., sg-xxxx,sg-yyyy).")

    if st.button("Launch EC2 Instance", key="launch_button"):
        if not key_pair_name:
            st.error("Please provide a Key Pair Name.")
        elif not security_group_ids_input_launch:
            st.error("Please provide at least one Security Group ID.")
        else:
            security_group_ids_launch = [sg.strip() for sg in security_group_ids_input_launch.split(',')]
            
            st.write("Attempting to launch instance...")
            try:
                with st.spinner("Launching... This may take a moment."):
                    response = ec2.run_instances(
                        ImageId=ami_id,
                        MinCount=1,
                        MaxCount=1,
                        InstanceType=instance_type,
                        KeyName=key_pair_name,
                        SecurityGroupIds=security_group_ids_launch,
                        TagSpecifications=[
                            {
                                'ResourceType': 'instance',
                                'Tags': [
                                    {
                                        'Key': 'Name',
                                        'Value': instance_name
                                    },
                                    {
                                        'Key': 'CreatedBy',
                                        'Value': 'StreamlitApp'
                                    }
                                ]
                            }
                        ]
                    )

                instance_id = response['Instances'][0]['InstanceId']
                st.success(f"Instance '{instance_name}' ({instance_type}) launched successfully!")
                st.write(f"**Instance ID:** `{instance_id}`")
                st.write(f"You can monitor its status in the AWS EC2 console.")

                st.subheader("Launched Instance Details:")
                st.json(response['Instances'][0])

            except ClientError as e:
                error_code = e.response.get("Error", {}).get("Code")
                error_message = e.response.get("Error", {}).get("Message")
                st.error(f"Error launching instance: `{error_code}` - {error_message}")
                st.warning("Please check your AWS credentials, AMI ID, Key Pair, Security Group IDs, and region.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    st.markdown("---")

    # --- Section for Terminating Instances ---
    st.header("Terminate Existing Instance(s)")

    instance_ids_to_terminate_input = st.text_input(
        "Instance ID(s) to Terminate (comma-separated)",
        "",
        key="terminate_ids"
    )
    st.warning("Terminating instances is irreversible. Please double-check the Instance IDs.")

    if st.button("Terminate EC2 Instance(s)", key="terminate_button"):
        if not instance_ids_to_terminate_input:
            st.error("Please enter at least one Instance ID to terminate.")
        else:
            instance_ids_to_terminate = [
                i.strip() for i in instance_ids_to_terminate_input.split(',') if i.strip()
            ]

            if not instance_ids_to_terminate:
                st.error("No valid Instance IDs entered for termination.")
            else:
                st.write(f"Attempting to terminate: {', '.join(instance_ids_to_terminate)}")
                try:
                    with st.spinner("Terminating..."):
                        response = ec2.terminate_instances(InstanceIds=instance_ids_to_terminate)
                    
                    terminated_instances = response.get('TerminatingInstances', [])
                    
                    if terminated_instances:
                        st.success("Successfully initiated termination for the following instances:")
                        for instance in terminated_instances:
                            st.write(f"- `{instance['InstanceId']}` (Current State: {instance['CurrentState']['Name']})")
                        st.info("It may take a few minutes for instances to fully terminate.")
                        st.json(terminated_instances)
                    else:
                        st.warning("No instances were listed as terminating. Check IDs and permissions.")

                except ClientError as e:
                    error_code = e.response.get("Error", {}).get("Code")
                    error_message = e.response.get("Error", {}).get("Message")
                    st.error(f"Error terminating instance(s): `{error_code}` - {error_message}")
                    st.warning("Please check your AWS credentials, Instance IDs, and region.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")


        