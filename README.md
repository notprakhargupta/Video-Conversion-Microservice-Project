Here’s the `README.md` file for your project:

```markdown
# Video Conversion Microservice Project

This project implements a **microservice-based video conversion system** using **Flask**, **RabbitMQ**, **Docker**, **Kubernetes**, and **FFmpeg**. The system allows users to upload videos and have them converted into various formats (e.g., MP3, 360p, 144p, etc.).

### Key Features:
- **Video Upload Service**: Users can upload video files.
- **Gate Service**: Acts as an intermediary, forwarding the conversion request from the Upload Service to the Conversion Service.
- **Video Conversion Service**: Converts uploaded videos into different formats such as MP3, 360p, 144p, etc.
- **RabbitMQ**: Used for communication between services (Upload, Gate, and Conversion).
- **Docker**: Containerizes each service for easy deployment.
- **Kubernetes**: Manages and orchestrates containers, ensuring scalability and availability.

---

## Architecture

The application is built with the following components:
1. **Video Upload Service** (Flask): Accepts video uploads, saves the files, and sends a message to RabbitMQ to trigger the video conversion process.
2. **Gate Service** (Flask): Listens for messages from the Upload Service and forwards the conversion request to the Conversion Service.
3. **Video Conversion Service** (Flask): Receives conversion requests, processes the video using FFmpeg, and saves the converted videos.
4. **RabbitMQ**: Acts as a message broker to facilitate communication between services.
5. **Kubernetes**: Deploys the services in separate pods and handles scaling and networking.

---

## Prerequisites

Before getting started, ensure you have the following installed:

- **Docker**: To build and run containers.
- **Kubernetes**: To manage the services and deploy them.
- **kubectl**: The command-line tool to interact with Kubernetes.
- **FFmpeg**: Required for video conversions (inside the container).

---

## Getting Started

### 1. Clone the repository:
```bash
git clone https://github.com/notprakhargupta/Video-Conversion-Microservice-Project.git
cd Video-Conversion-Microservice-Project
```

### 2. Build Docker Images for Each Service:

Make sure to build the Docker images for each of the services (Upload Service, Gate Service, and Conversion Service):

```bash
docker build -t your-repo/upload-service -f Dockerfile .
docker build -t your-repo/gate-service -f Dockerfile .
docker build -t your-repo/conversion-service -f Dockerfile .
```

### 3. Push Docker Images to Your Registry:

After building the images, push them to your container registry (e.g., Docker Hub, AWS ECR, etc.):

```bash
docker push your-repo/upload-service
docker push your-repo/gate-service
docker push your-repo/conversion-service
```

### 4. Set Up Kubernetes Cluster:

Make sure you have a running Kubernetes cluster. If you are using **Minikube** locally, you can start it using:

```bash
minikube start
```

### 5. Deploy RabbitMQ:

Run the RabbitMQ deployment:

```bash
kubectl apply -f rabbitmq-deployment.yaml
```

This will create a RabbitMQ pod and expose the service within the Kubernetes cluster.

### 6. Deploy the Microservices:

Now, deploy the **Upload Service**, **Gate Service**, and **Conversion Service**:

```bash
kubectl apply -f upload-service-deployment.yaml
kubectl apply -f gate-service-deployment.yaml
kubectl apply -f conversion-service-deployment.yaml
```

### 7. Expose the Services:

To expose the services, you can create **LoadBalancer** or **NodePort** services. Optionally, you can configure **Ingress** to route traffic.

For example, you can expose the **Upload Service** via a **LoadBalancer**:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: upload-service
spec:
  selector:
    app: upload-service
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
```

Apply the configuration:

```bash
kubectl apply -f upload-service-loadbalancer.yaml
```

### 8. Verify the Deployment:

To ensure everything is running as expected, check the status of your pods:

```bash
kubectl get pods
```

Check the status of services:

```bash
kubectl get services
```

Check logs for any errors:

```bash
kubectl logs <pod-name>
```

---

## How It Works

1. **User Uploads Video**:
   - The user uploads a video via the **Upload Service**'s `/upload` endpoint.
   - The video is saved, and a message is sent to **RabbitMQ**, notifying the **Gate Service**.

2. **Gate Service Forwards Request**:
   - The **Gate Service** listens for messages from RabbitMQ.
   - It forwards the conversion request to the **Conversion Service**.

3. **Video Conversion**:
   - The **Conversion Service** receives the video conversion request and uses **FFmpeg** to convert the video into the specified formats (e.g., MP3, 360p, 144p).
   - The converted video is saved in the `/converted` folder under a user-specific subfolder.

4. **Download Converted Videos**:
   - Once the video is converted, the user can download it from the provided URL.

---

## Scaling the Services

Kubernetes allows you to scale each service independently. For instance, to scale the **Upload Service** to 3 replicas, you can run the following command:

```bash
kubectl scale deployment upload-service --replicas=3
```

This will ensure the Upload Service can handle higher loads by running multiple instances.

---

## Conclusion

This project demonstrates how to use **Flask**, **RabbitMQ**, **Docker**, and **Kubernetes** to build a scalable and distributed video conversion service. Each service is containerized and can be managed independently in a Kubernetes cluster.

You can extend this system further by adding more video formats, different resolution options, error handling, and user authentication.

---

## Contact

Feel free to open issues or contribute to the project. If you have any questions or need further assistance, you can reach out to the repository owner or raise an issue.

---

This `README.md` provides a comprehensive guide to deploying the video conversion system, including setup instructions, service architecture, and scaling options.
