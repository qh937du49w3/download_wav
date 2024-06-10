#  參考文件
#  https://learn.microsoft.com/en-us/python/api/overview/azure/cognitiveservices-vision-computervision-readme?view=azure-python-previous
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
import os
import azure.cognitiveservices.speech as speechsdk


IMAGE = 'https://tse3.mm.bing.net/th?id=OIP.AzOTg_vwnMEZNYlr7KQFEwHaJZ&pid=Api&P=0&h=180' # 影像

# 以下資訊可以從 Azure 電腦視覺服務取得(正式上線時不要直接把金鑰跟服務端點寫在程式碼裡)
C_KEY = 'a9f76e3e1cee413ab3ce8af8d9110ad8' # 填入金鑰
C_ENDPOINT = 'https://vision10173237.cognitiveservices.azure.com/' # 填入端點

# 以下資訊可以從 Azure 翻譯服務取得(正式上線時不要直接把金鑰跟服務端點寫在程式碼裡)
T_REGION = 'eastus' # 填入位置/區域
T_KEY = '27a4001fd3fd4914b5333f66427e5800' # 填入金鑰
T_ENDPOINT = 'https://api.cognitive.microsofttranslator.com/' # 填入文字翻譯的 Web API

# speech 的key and region
SPEECH_KEY = "2729a16c3dc9489fa2b0df48d9d2c0a3"
SERVICE_REGION = "eastus"

def ImageAnalysis(image):
    client = ComputerVisionClient(
        endpoint=C_ENDPOINT,
        credentials=CognitiveServicesCredentials(C_KEY)
    )
    analysis = client.describe_image(url=image, max_candidates=1, language="en")

    return analysis.captions[0]

def Translator(target):
    text_translator = TextTranslationClient(
        endpoint=T_ENDPOINT,
        credential=TranslatorCredential(T_KEY, T_REGION)
    )
    targets = []
    targets.append(InputTextItem(text=target))

    responses = text_translator.translate(content=targets, to=["zh-hant"], from_parameter="en")
    
    return responses


def text_to_speech(text,filename = "output.wav"):
    # 創建語音配置對象
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)
    #輸出成.wav
    audio_config = speechsdk.audio.AudioOutputConfig(filename = filename)
    # 創建語音合成器
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,audio_config=audio_config)
    # 合成語音並播放
    speech_synthesizer.speak_text_async(text).get()
    return filename

    
text_en = ImageAnalysis(IMAGE)
text_zh_Hant = Translator(text_en.text)
final_text = (text_zh_Hant[0].translations[0].text)
print(final_text)
text_to_speech(final_text)
