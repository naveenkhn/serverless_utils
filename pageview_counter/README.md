# pageview_counter

This project implements a simple serverless page view counter using AWS Lambda, API Gateway, and DynamoDB. It is deployed using the AWS Serverless Application Model (SAM CLI).

## Project Structure

- `pageview_counter/` - Contains the Lambda function logic (`app.py`)
- `template.yaml` - Defines the Lambda function, API Gateway, and other AWS resources
- `.gitignore` - Excludes build artifacts, virtual environments, and editor metadata
- `events/` - Sample event payloads (optional)

## Deployment

### Initial Setup

If this is your first time creating the SAM project, initialize it using:

```bash
sam init
```

To build and deploy this application:

```bash
sam build
sam deploy --guided
```

The `--guided` flag walks through configuration options such as stack name, region, and IAM capabilities. Once entered, these settings are saved to `samconfig.toml` for future deployments.


### API Usage

After deployment, the API is available at:

```
https://<api-id>.execute-api.<region>.amazonaws.com/Prod/visit/
```

Each `GET` request to `/visit` increments the `views` counter for the page "home" stored in DynamoDB and returns the updated count.

## Requirements

- AWS CLI configured with access keys
- AWS SAM CLI
- Python 3.9 or later
- Docker (for local builds)

## Cleanup

To delete the stack:

```bash
sam delete
```

## DynamoDB Management

Useful AWS CLI commands for inspecting and modifying the DynamoDB `pageview_counter` table:

### Get current view count
```bash
aws dynamodb get-item \
  --table-name pageview_counter \
  --key '{"page": {"S": "home"}}' \
  --region ap-south-1
```

### Reset view count to zero
```bash
aws dynamodb update-item \
  --table-name pageview_counter \
  --key '{"page": {"S": "home"}}' \
  --update-expression "SET #v = :zero" \
  --expression-attribute-names '{"#v": "views"}' \
  --expression-attribute-values '{":zero": {"N": "0"}}' \
  --region ap-south-1
```

### Describe table
```bash
aws dynamodb describe-table \
  --table-name pageview_counter \
  --region ap-south-1
```

### List tables
```bash
aws dynamodb list-tables \
  --region ap-south-1
```

### Fetch Lambda logs
```bash
aws logs describe-log-streams \
  --log-group-name "/aws/lambda/pageview-counter-PageviewCounterFunction-<unique-suffix>" \
  --order-by LastEventTime \
  --descending \
  --limit 1
```

```bash
aws logs get-log-events \
  --log-group-name "/aws/lambda/pageview-counter-PageviewCounterFunction-<unique-suffix>" \
  --log-stream-name "<latest-log-stream-name>"
```

## License

MIT
