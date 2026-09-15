import json, boto3
bedrock = boto3.client('bedrock-agent-runtime')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ChezaStemEd_ChatHistory')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    question = body['question']
    
    # RAG from Bedrock Knowledge Base - replace KB_ID
    response = bedrock.retrieve_and_generate(
        input={'text': question},
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': 'YOUR_KB_ID',
                'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0'
            }
        }
    )
    answer = response['output']['text']
    table.put_item(Item={'student_id': 'eldoret_student', 'question': question, 'answer': answer})
    
    return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'answer': answer})}