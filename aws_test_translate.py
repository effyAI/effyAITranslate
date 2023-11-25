import boto3

translate = boto3.client('translate', region_name="us-east-1")

result = translate.translate_text(Text="Hello, World", SourceLanguageCode="en", TargetLanguageCode="hi")
print(result.get('TranslatedText'))