
```markdown
# Three-Tier Microservices Application on AWS

This project demonstrates a **lightweight three-tier architecture** deployed on AWS using ECS Fargate, RDS, ECR, and S3.  
It consists of:
- **Frontend (Presentation Layer):** Static `index.html` hosted in Amazon S3 bucket (Static Website Hosting).
- **Application Layer:** Two microservices (`user-service` and `product-service`) running on AWS ECS Fargate.
- **Data Layer:** Two RDS MySQL databases (`users_db` and `products_db`).

---
## 📂 Project Structure
```
```

three-tier-app/
│
├── user-service/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── product-service/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml   (for local testing)
└── README.md

```
---

## 🚀 Deployment Steps

### 1. Build and Push Images to ECR
```bash
# Authenticate Docker with ECR
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <account_id>.dkr.ecr.ap-south-1.amazonaws.com

# Build and push user-service
docker build -t user-service ./user-service
docker tag user-service:latest <account_id>.dkr.ecr.ap-south-1.amazonaws.com/user-service:latest
docker push <account_id>.dkr.ecr.ap-south-1.amazonaws.com/user-service:latest

# Build and push product-service
docker build -t product-service ./product-service
docker tag product-service:latest <account_id>.dkr.ecr.ap-south-1.amazonaws.com/product-service:latest
docker push <account_id>.dkr.ecr.ap-south-1.amazonaws.com/product-service:latest
````

---

### 2. Create Databases (RDS)

* Create **RDS MySQL instance** for `users_db` and `products_db`.
* Note the **endpoint, username, and password**.

---

### 3. Create ECS Cluster & Task Definitions

* **Cluster:** `three-tier-cluster`
* **Task Definitions:**

  * `user-service-task`

    * Image: `user-service` ECR URI
    * Port: `5000`
    * Env Vars: `DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME`
  * `product-service-task`

    * Image: `product-service` ECR URI
    * Port: `6000`
    * Env Vars: `DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME`
* Enable logging with CloudWatch.

---

### 4. Create ECS Services

* Launch 1 task for each service.
* Attach security group rules:

  * Allow **HTTP (5000, 6000)** inbound.
  * Allow outbound to RDS.

---

### 5. Frontend with S3

* Create an **S3 bucket** → Enable **Static Website Hosting**.
* Upload `index.html`.
* In `index.html`, update API URLs:

  ```javascript
  const USER_API = "http://<user-service-public-ip>:5000/users";
  const PRODUCT_API = "http://<product-service-public-ip>:6000/products";
  ```
* Access frontend via S3 website endpoint.

---

## ✅ How it Works

1. User opens `index.html` hosted in **S3**.
2. Frontend makes API calls to **user-service** and **product-service** running on ECS.
3. Services interact with their respective **RDS databases**.
4. Responses are sent back to frontend for display.

---

## ⚡ Notes

* Free Tier Safe: 1 task per service + small RDS + S3 static hosting.
* Security Groups: Ensure ECS services can talk to RDS.
* Update `index.html` whenever ECS public IP changes (for production, ALB + Route53 is recommended).

```
```
