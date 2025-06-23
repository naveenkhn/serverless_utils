# pageview_counter

This project implements a simple serverless page view counter using AWS Lambda, API Gateway, and DynamoDB. It is deployed using the AWS Serverless Application Model (SAM CLI).

## Project Structure

- `pageview_counter/` - Contains the Lambda function logic (`app.py`)
- `template.yaml` - Defines the Lambda function, API Gateway, and other AWS resources
- `.gitignore` - Excludes build artifacts, virtual environments, and editor metadata
- `events/` - Sample event payloads (optional)

## Deployment

To build and deploy this application, use the following commands:

```bash
sam build --use-container
sam deploy --guided
```

After deployment, the function will be accessible via the generated API Gateway URL at the `/visit` path. Each visit increments a counter stored in DynamoDB and returns the updated value.

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

## License

MIT
