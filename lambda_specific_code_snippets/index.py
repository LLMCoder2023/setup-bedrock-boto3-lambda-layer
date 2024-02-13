import json
import boto3

def setup_bedrock_runtime():
    session = boto3.Session()

    bedrock = session.client(
        service_name='bedrock-runtime',
        region_name='us-west-2',
    )
    return bedrock

def lambda_handler(event, context):

    """
        define user prompt from test event.

        Lambda Test Event:
        {
            "prompt":"Tell me about blackholes"
        }
    """
    user_prompt = event['prompt']

    # Setup AWS SDK for Python
    boto3_bedrock = setup_bedrock_runtime()

    # Concatenate Claude's prompt template with the user's input'
    prompt=f"""Human: {user_prompt}
    Assistant:
    """

    #select your bedrock model
    bedrock_model_id="anthropic.claude-instant-v1"

    # define your inference parameters
    claude_inference_configuration = {
        'temperature': 0.1,
        'top_p': 0.999,
        'top_k': 250,
        'max_tokens_to_sample': 200,
        'prompt': prompt
    }

    # setup request payload
    payload = json.dumps(claude_inference_configuration)
    body = payload
    accept = 'application/json'
    contentType = 'application/json'

    #invoke bedrock
    response = boto3_bedrock.invoke_model(
        body=body,
        modelId=bedrock_model_id,
        accept=accept,
        contentType=contentType
    )

    # load response into a json object
    response_body = json.loads(response.get('body').read())

    # print out the response for debugging purposes (this shows up in the lambda execution result)
    print(response_body)

    # Return Lambda Response
    return {
        'statusCode': 200,
        'body': response_body['completion']
    }
