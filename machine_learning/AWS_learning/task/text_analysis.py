#Entity Extraction
# Importing Boto3
import boto3
import json

text = """
*I am currently close to completing my Post Graduate Diploma in Data Science from IIIT Bangalore in collaboration with UpGrad and therefore I feel I can throw some light on the program and help others make an informed decision on choosing programs offered by UpGrad.*

*Prior to taking up the course with UpGrad, I had done a few courses from edX and Coursera platforms posted by various Universities across the globe. This, I combined with online resources and study material in hopes of making a career transition to Data Science. The fact is, we have all the required resources available online such as video material for teaching the technology, data sets to gain coding knowledge and other materials to teach us about the business domain. Honestly, after about 4 months of trying to crack data science this way (the hard way), it didn’t seem like I was making any headway. I was nowhere close to understanding an industry which is not an IT discipline at all, but rather a field which combines Mathematics, Coding and above all Business domain.*

*This is when I found out about the PGDDS course offered by UpGrad which provided a definite structure in the vast ocean of information about the Data Science Industry available online. It gave the benefit of a structured program rather than spending or wasting huge amounts of time just trying to accumulate all the resources required to make some headway. Simply put, it saved me the effort of searching for needles in a mammoth haystack (internet).*

*So I signed up for the program and after completing 10 months of the 11 month program, here are the few benefits I have felt.*

*1. First and foremost, this is not a certification course but a Post Graduate Diploma provided by an accredited University that carries a lot of value than any certification course. Let’s be honest, any company would always value a university degree over any online certification course.*

*2. Faculty who teach different modules are top notch in their fields having Doctorate or Master’s degree. Further, since Data Science is inter-disciplinary in nature, therefore we would require faculties with experience in the relevant disciplines to guide us. IIIT-B in collaboration with UpGrad have chosen faculties with the right qualification to match with the different disciplines.*

*3. Moreover, UpGrad has tied up with industry professionals working at companies such as Gramener, Uber, Flipkart etc. to provide the students with a course that makes it more aligned with the happenings in the current Data Science Industry. They also let you work on case studies using real time data (as opposed to fabricated data) providing us with exposure to actual problems in the industry being solved using Data Analytics.*

*4. UpGrad has further tied up with a third party company known as Tapchief to allow us to interact with top professionals in the industry. This is aimed at giving us guidance on how we can further our career in the field considering our educational qualification, past experiences, our expectation or goals, and age. They also help in guiding us in our final Capstone Project through video chats and main benefit of this is to guide us in terms of realistic approaches to the problem and providing business insights into the given problems.*

*5. Biggest benefit: Networking!!! The biggest benefit I have received is being able to collaborate with so many other students who are industry professionals at different stages of the course. Numerous opportunities are given to interact with this diverse group of people such as working in groups on numerous case studies, meeting them at basecamps arranged by UpGrad and lot of us can meet up at campus library if you are from Bangalore.*

*UpGrad is trying to tackle a concern or a problem which has been voiced by so many CEO’s of top IT organizations: EMPLOYABILITY. They do this by collaborating not just with an academic institute, but also bringing in industry experts to give us the right tools required in the market.*

*I understand the course fees are on the upper side compared to many other online and offline courses offered, but I don’t personally believe there are many platforms which offer a holistic package such as the one’s UpGrad offered.*

*I hope this review helps anyone wishing to pursue a course offered by UpGrad and I must say, taking up any of the courses is serious business and will require serious time and effort from the candidates.

"""
client = boto3.client('comprehend', aws_access_key_id="AKIAWZ42OIVQELVZVQQZ",aws_secret_access_key= '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')
print('Calling DetectKeyPhrases')
context = json.dumps(client.detect_key_phrases(Text=text, LanguageCode='en'), sort_keys=True, indent=4)
print(context)
print('End of DetectKeyPhrases\n')

#### Question 2.

# Which of the following companies is not listed in the review?
#
# - upGrad
# - Gramener
# - Flipkart
# - Ola
entities = client.detect_entities(Text = text, LanguageCode = 'en') #API call for entity extraction
entities = entities['Entities'] #all entities
print(entities)
textEntities = [dict_item['Text'].lower() for dict_item in entities] #the text that has been identified as entities
typeEntities = [dict_item['Type'] for dict_item in entities] #the type of entity the text is
input_companies = ['upGrad', "Gramener", "Flipkart", "Ola"]
not_listed_companies = []
for item in input_companies:
    if item.lower() not in set(textEntities):
        not_listed_companies.append(item)
print("Following companies are not listed in the review", not_listed_companies)

# Based on the results from sentiment analysis using Amazon Comprehend,
# select the most appropriate option from the ones given below.
response = client.batch_detect_sentiment(
    TextList=[
        text,
    ],
    LanguageCode='en'
)

print(response)
print(response['ResultList'][0]['Sentiment'])
