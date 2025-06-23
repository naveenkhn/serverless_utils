# AWS Lambda Functions

## 1. What is AWS Lambda?

AWS Lambda is a **serverless compute service** that lets you run code without provisioning or managing servers. You only pay for the compute time you consume — there is no charge when your code is not running. It's ideal for lightweight, event-driven use cases such as APIs, file processing, notifications, and more.

In this repository (`serverless_utils`), you'll find Lambda function implementations — starting with the `pageview_counter`, and more to come.

---

## 2. How to Create a Lambda Function (with AWS SAM)

This project uses the **AWS Serverless Application Model (SAM)** CLI.

### 🛠️ Step-by-Step Guide

#### a. Initialize a project
```bash
sam init
```

#### b. Build the function
```bash
sam build
```

#### c. Deploy (guided)
```bash
sam deploy --guided
```

This command will:
- Package your code and dependencies
- Upload it to S3
- Create or update CloudFormation stack
- Deploy the Lambda, API Gateway (if defined), and other resources

Once deployed, the Lambda will be live and triggered based on the defined event source (e.g., HTTP request).

---

## 3. How does Lambda work behind the scenes?

When a Lambda function is triggered:

1. **AWS provisions a lightweight container** (if not already warm) and loads your function code.
2. It **executes the handler method** with the event payload.
3. The Lambda **terminates or stays warm** depending on future traffic.

Under the hood:
- API Gateway → triggers the Lambda
- IAM roles → grant permissions to access services (e.g., DynamoDB)
- CloudWatch → captures logs from Lambda executions
- CloudFormation → manages all infrastructure as code

---

## 3.1 Performance Overhead & Limitations

### ⏱️ Performance Overhead
- **Cold Starts**: The first request after a period of inactivity may experience a delay (typically 100ms to a few seconds) while AWS provisions a container.
- **Stateless Execution**: Lambda functions do not retain memory or local state between invocations.
- **Limited Execution Time**: Maximum duration is 15 minutes per invocation.
- **Concurrent Execution Limits**: There is an account-level limit on the number of concurrent executions (can be increased by request).

### 🚧 Limitations
- **Memory and Storage**:
  - Memory: 128 MB to 10 GB
  - Temporary `/tmp` storage: up to 512 MB (can be increased to 10 GB)
- **Package Size**: Deployment package (zipped) must be less than 50 MB for direct upload or 250 MB when using S3.
- **Environment Variables**: Max size is 4 KB.
- **No direct support for GPUs**: Lambda doesn’t support GPU acceleration for workloads.

Use cases with heavy compute, long-running tasks, or needing persistent connections (e.g., WebSockets or stateful apps) may not be a good fit for Lambda.

---

### 3.2 How does Lambda handle concurrent events?

AWS Lambda is designed for horizontal scalability. When multiple events (e.g., HTTP requests) occur simultaneously:

- **Each event triggers a separate invocation** of the Lambda function.
- Lambda can spin up multiple containers to handle these in parallel.
- AWS allows for up to **1,000 concurrent executions per region by default** (soft limit).

In the case of the `pageview_counter`:
- Each visitor to the portfolio page triggers a Lambda run.
- The counter is updated using DynamoDB's `ADD` operation, which is **atomic**.
- Even with high concurrency, **DynamoDB ensures accurate view counts** via serialized, thread-safe operations.

This ensures that spikes in traffic are handled gracefully without data corruption or missed updates.

---

## 4. Example: `pageview_counter`

This function:
- Is triggered via an HTTP GET request
- Increments a page counter stored in DynamoDB
- Returns the updated count

**Endpoint**:  
```
https://<api-id>.execute-api.ap-south-1.amazonaws.com/Prod/visit/
```

### 🔧 Useful AWS CLI Commands

Reset views:
```bash
aws dynamodb update-item \
  --table-name pageview_counter \
  --key '{"page": {"S": "home"}}' \
  --update-expression "SET #v = :zero" \
  --expression-attribute-names '{"#v":"views"}' \
  --expression-attribute-values '{":zero": {"N": "0"}}' \
  --region ap-south-1
```

Get current views:
```bash
aws dynamodb get-item \
  --table-name pageview_counter \
  --key '{"page": {"S": "home"}}' \
  --region ap-south-1
```

---

## 5. Monitoring

Use CloudWatch Logs to check invocation logs:
```bash
aws logs describe-log-streams \
  --log-group-name "/aws/lambda/<function-name>" \
  --order-by LastEventTime \
  --descending \
  --limit 1
```

```bash
aws logs get-log-events \
  --log-group-name "/aws/lambda/<function-name>" \
  --log-stream-name "<latest-stream-name>"
```

---

