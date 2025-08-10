def run():  
    import streamlit as st
    from kubernetes import client, config
    from kubernetes.client.rest import ApiException

    # Load kubeconfig (works for Minikube too)
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        apps_v1 = client.AppsV1Api()
    except Exception as e:
        st.error(f"Error loading kubeconfig: {e}")
        st.stop()

    st.title("📦 Kubernetes Dashboard (Minikube)")

    menu = st.sidebar.radio("📌 Select an action", [
        "List Pods",
        "Create Pod",
        "Delete Pod",
        "List Nodes",
        "List Deployments",
        "List Services"
    ])

    # ---------- MENU: LIST PODS ----------
    if menu == "List Pods":
        st.subheader("📜 Pods in 'default' namespace")
        try:
            pods = v1.list_namespaced_pod(namespace="default")
            pod_data = []
            for pod in pods.items:
                pod_data.append({
                    "Name": pod.metadata.name,
                    "Status": pod.status.phase,
                    "Node": pod.spec.node_name,
                    "IP": pod.status.pod_ip
                })
            st.table(pod_data)
        except ApiException as e:
            st.error(f"Error listing pods: {e}")

    # ---------- MENU: CREATE POD ----------
    elif menu == "Create Pod":
        st.subheader("➕ Create a new Pod")
        pod_name = st.text_input("Pod Name", "my-pod")
        pod_image = st.text_input("Container Image", "nginx")
        if st.button("Create Pod"):
            pod_manifest = {
                "apiVersion": "v1",
                "kind": "Pod",
                "metadata": {"name": pod_name},
                "spec": {
                    "containers": [{
                        "name": pod_name,
                        "image": pod_image,
                        "ports": [{"containerPort": 80}]
                    }]
                }
            }
            try:
                v1.create_namespaced_pod(namespace="default", body=pod_manifest)
                st.success(f"✅ Pod '{pod_name}' created successfully!")
            except ApiException as e:
                st.error(f"Error creating pod: {e}")

    # ---------- MENU: DELETE POD ----------
    elif menu == "Delete Pod":
        st.subheader("🗑 Delete a Pod")
        pods = v1.list_namespaced_pod(namespace="default").items
        pod_list = [p.metadata.name for p in pods]
        pod_to_delete = st.selectbox("Select Pod", pod_list)
        if st.button("Delete Pod"):
            try:
                v1.delete_namespaced_pod(name=pod_to_delete, namespace="default")
                st.success(f"🗑 Pod '{pod_to_delete}' deleted successfully!")
            except ApiException as e:
                st.error(f"Error deleting pod: {e}")

    # ---------- MENU: LIST NODES ----------
    elif menu == "List Nodes":
        st.subheader("💻 Nodes")
        try:
            nodes = v1.list_node()
            node_data = []
            for node in nodes.items:
                node_data.append({
                    "Name": node.metadata.name,
                    "Status": node.status.conditions[-1].type,
                    "Kubelet Version": node.status.node_info.kubelet_version
                })
            st.table(node_data)
        except ApiException as e:
            st.error(f"Error listing nodes: {e}")

    # ---------- MENU: LIST DEPLOYMENTS ----------
    elif menu == "List Deployments":
        st.subheader("📦 Deployments")
        try:
            deployments = apps_v1.list_namespaced_deployment(namespace="default")
            dep_data = []
            for dep in deployments.items:
                dep_data.append({
                    "Name": dep.metadata.name,
                    "Replicas": dep.status.replicas,
                    "Available": dep.status.available_replicas
                })
            st.table(dep_data)
        except ApiException as e:
            st.error(f"Error listing deployments: {e}")

    # ---------- MENU: LIST SERVICES ----------
    elif menu == "List Services":
        st.subheader("🔌 Services")
        try:
            services = v1.list_namespaced_service(namespace="default")
            svc_data = []
            for svc in services.items:
                svc_data.append({
                    "Name": svc.metadata.name,
                    "Type": svc.spec.type,
                    "Cluster IP": svc.spec.cluster_ip,
                    "Ports": str(svc.spec.ports)
                })
            st.table(svc_data)
        except ApiException as e:
            st.error(f"Error listing services: {e}")



        
