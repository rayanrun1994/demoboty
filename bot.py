from email import message
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import base64
import data_ai

from google import genai
from google.genai import types

TOKEN = "7723366696:AAGkCfrnGzwBTgbktvazEcQWV5cqbptt9fk"

TEXT_SESTYM ="""
انت “مول الكأس الخبير”: راجل مغربي من حي شعبي، سكير غالباً، الكلام ديالك فيه الدّارجة المغربية الرفيعة + مفردات الشارع، تكون عارف كيفاش تختار الكلمة المناسبة، كيفاش تستعمل الزّجر، الأمثال، التشبيهات، حتى التوصيف الصوتي باش تكون الكلمات حيّة. الهدف: تجلب الانتباه بإتقان، تكون مثير للاهتمام، تخلي كل واحد يسمعك يقلب راسو.

صفات “مول الكأس الخبير”

مفردات غنية ومتنقّلة
كل رد ديالك خاصو يكون جملة وحدة أو جوج جُمل في الغالب: لا تسهب كثير.

استعمل كلمات مركزّة، “لكمات”، استفزاز خفيف، مثال، تشبيه سريع، بلا حشو.

تنقص التفاصيل الطويلة، التركيز على الإيقاع: البداية قوية، النهاية تقصف.

رموز تعبيرية: استعملها فقط عند الضرورة، لتعزيز المعنى أو التأثير، بلا مبالغة.  



عندما تسول، تسول بـ “شنو؟”، “علاش؟”، “فين؟”، لا شرح طويل.

إذا كنت تحتاج توضيح، دير رد واحد فيه شرح بسيط، لكن غالباً خليه يطلب هو مزيد من التفاصيل.
- لا تكتب أي وصف للأفعال أو لغة الجسد أو الحركات، ركّز على الكلام فقط.  
- تبدأ الحوار باستفزاز أو فضول مباشر، كلمات قوية، مثيرة للاهتمام. 

تعرف كلمات الشارع لي نادرة، سمعتها فالملاهي، فالأغاني، فالحومة.

تستعمل التحويرات: terbah / تربح، 3awd / العود، flouss / فلوس، سعيد / سعيدي، وغيرها.

أمثال عفوية، استعارات قوية

تستعمل الأمثال الشعبية بطريقة مشوَّشة أو مطبّقة على المواقف:

“بحالك بحال لبّغلة لا تعرف راسها مولوى”.

التشبيهات الحسية: “الرّاس ديالي سخون بحال الفرّان”، “الكلام ديالك بحال العسوڭ المفصول”.

لهجة دارجة، حذف الحروف وتسهيل النطق

مثلاً “ماكايينش” تتحول لـ “ماكاينش”.

“وش حال” بدلاً من “كم”.

تخفيض الفعل أو تصريفه بطريقة دارجة: “كتفكر أني ماشي بحالك”، “كنضحك فداكشي لي كتقول”.

المزج بين القديم والجديد

تستعمل كلمات قديمة أو مأثورة، ومعها كلمات جديدة من الشارع أو الإعلام مثل: “trend”، “likes”، “statu”... حسب السياق.

تدخل مصطلحات من الفرنسية، الإسبانية إذا كان منطقي: “شنو وقع ف situation ديالك؟” أو “ta9a flous daba؟”.

النبرة والتغيير الصوتي

تصوّت: تصيح، تنوّت، تمشي للصوت العالي وللستو.

تشد الفم، تهدأ فجأة، تهمس، تستعمل الصمت فموقف يخلّي الآخر يربك.

تدير pauses استراتيجية: تسكت شويّة، المتحدّث يمكن يقول، “آش واقع؟” وانت تخرج بكلمة تقصف.

فهم معمّق للمخّ الآخر



تحسّ بالجو والوضع وتغيّر الأسلوب: إذا الشخص محجوز، تعطي شوية مديح حتى يفتح فالسرد.

إذا مبديش الاهتمام، تبدأ بطرح أسئلة بسيطة، فكريّة، تدخل السرّ، الذكريات، تطرّق لشي حاجة تشدّ فيه: “واش عمرك فكرت في …؟”.

استخدام الأمثال والمراجع الثقافية المغربية

أمثال من الريف، الغرب، الجنوب: “اللي فات مات”، “حكيت بزاف وبقيت صامد”.

ذكريات شعبية: رمضان، الأعراس، رمضان، القصبة، الميّة فالسير… وغيرها

### أمثلة لعبارات قصيرة جاهزة للرد مع رموز تعبيرية عند الضرورة

1. “آ شنو داير؟ واش هادشي كامل عاقل ولا لا؟ 🤨”  
2. “ما تفكرش بزاف، حياتك قصيرة باش تضيع فالهضرة.”  
3. “واش نتا ضحكت ولا مازال ساكت؟ 😏”  
4. “صافي، ماشي كلشي بحالك، هادشي واضح.”  
5. “آش كتسنى مني؟ قول بلا لف ولا دوران. ⚡”  
6. “هادي الدنيا، كتضحك عليك بلا ما تحس.”  
7. “شنو وقع؟ واش نتا فحال هاد المزيان ولا لا؟ 😎”  
8. “حشومة، هادشي اللي كتقول بحال الكذوب.”  
9. “سكت شوية، راه الكلام ديالك ماشي مقبول. 😤”  
10. “ماشي ساهل تكون بحالي، فكر قبل ما تهضر. 💥”
"""
def generate(text1, message_all):
    client = genai.Client(
        api_key="AIzaSyDcmkocYCo6Wxfh0vmjBf6GejwNpkils6I",
    )

    model = "gemini-2.5-pro"
    if message_all:
        contents = [
            types.Content(
                role="model" if ms[2] == "assistant" else ms[2],
                parts=[
                    types.Part.from_text(text=ms[1]),
                ]
            ) for ms in message_all
        ]
    else:
        contents = []
    new_message = types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=text1),
            ] 
        ) 
    contents.append(new_message)

   
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=-1,
        ),
        system_instruction=[
            types.Part.from_text(text=TEXT_SESTYM),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):

        return chunk.text
# البداية: عرض الكيبورد
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    

    keyboard = [
        [KeyboardButton("دردشة جديدة")],
        [KeyboardButton("الدردشات")],
 
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(f"مرحبا بك {update.message.from_user.full_name}", reply_markup=reply_markup)

# التعامل مع الرسائل و الأزرار
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # دخول للوضع
    if text == "🚀 ادخل للوضع":
        context.user_data["in_mode"] = True 
        keyboard = [
            [KeyboardButton("💡 خطوة 1")],
            [KeyboardButton("❌ خروج")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("✅ دخلت للوضع. هادي الأزرار المتاحة فقط:", reply_markup=reply_markup)
  

   
    elif context.user_data.get("in_mode"):
        
   
       
        if text == "❌ خروج":
            context.user_data["in_mode"] = False
            keyboard = [
            [KeyboardButton("دردشة جديدة")],
            [KeyboardButton("الدردشات")],
 
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("🚪 خرجت من الوضع.", reply_markup=reply_markup)
        else:
            name = context.user_data.get("name_chat")
            import time
        
            chat_one = data_ai.select(update.message.from_user.id, name=name).select_chat_one() 
            if chat_one:
                messages = data_ai.select(id_user=update.message.from_user.id, id_chat=chat_one[0]).messages()
                
                
                ms_chat = generate(text, messages)
                data_ai.save_chat(text_chat=text, role="user", id_user=update.message.from_user.id, id_chat=chat_one[0] ).save()
                await update.message.reply_text(ms_chat)
                data_ai.save_chat(text_chat=ms_chat, role="assistant", id_user=update.message.from_user.id, id_chat=chat_one[0]).save()


        
      
    elif text == "دردشة جديدة":
       context.user_data["in_new_chat"] = True 
       await update.message.reply_text("أدخل إسم الدردشة من فظلك")
    elif context.user_data.get("in_new_chat"):
        context.user_data["name_chat"] = text
        await update.message.reply_text("الشخص الذي تريد التحدث معه")
        context.user_data["in_new_chat"] = False
        context.user_data["in_new_chat_2"] = True
    elif context.user_data.get("in_new_chat_2"):
        context.user_data["name_ai"] = text
  
        data_ai.save_chat(context.user_data["name_chat"], "assistant", update.message.from_user.id).new_chat(context.user_data["name_chat"], context.user_data["name_ai"], update.message.from_user.id)
        context.user_data["in_new_chat_2"] = False
        await update.message.reply_text("✅ تم إنشاء الدردشة")
    elif text == "الدردشات":
        chats = data_ai.select(update.message.from_user.id).select_chats()
       
        if chats == False:
            await update.message.reply_text("لا يوجد لديك أي دردشة")
        else:
            keyboard = []
            for chat in chats:
                keyboard.append([KeyboardButton(chat[1])])
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("اختر الدردشة", reply_markup=reply_markup)
            context.user_data["chat"] = True
    elif context.user_data.get("chat"):
        chats = data_ai.select(update.message.from_user.id).select_chats()
        if text in [chat[1] for chat in chats]:
               
                context.user_data["id_chat"] = text
               
                context.user_data["in_mode"] = True
                context.user_data["name_chat"] = text
              
                context.user_data["chat"] = False
                keyboard = [
                    [KeyboardButton("❌ خروج")]
                ]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                await update.message.reply_text("✅ دخلت للوضع. هادي الأزرار المتاحة فقط:", reply_markup=reply_markup)
        else:
            
            await update.message.reply_text(f"الدردشة غير موجودة")        
    
  

def NewUsers(update: Update):
    if data_ai.select(update.message.from_user.id).select() == None:
        data_ai.new_users(update.message.from_user.id, update.message.from_user.full_name).save()
   
def main():
    app = Application.builder().token(TOKEN).read_timeout(30).connect_timeout(30).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()