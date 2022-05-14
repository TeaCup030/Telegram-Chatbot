# Bot Key
API_KEY = ''

URL = "https://api.telegram.org/bot{}/".format(API_KEY)

# Greeting
Greeting_welcome = "Hello"

# Loop Question Voice
# questions_string = list()
# for i in ['Forward','Backward']:
#     for j in range(1, 17):
#         questions_string.append(i + 'Q' + str(j) + ': Please input you heard number')

for_questions_string = list()
for i in ['Forward']:
    for j in range(1, 17):
        for_questions_string.append(i + 'Q' + str(j) + ': Please input you heard number')

back_questions_string = list()
for i in ['Backward']:
    for j in range(1,16):
        back_questions_string.append(i + 'Q' + str(j) + ': Please input you heard number')


# Greeting Q
Greeting_hau = "How are you ?"

Greeting_word = "My name is Mandy. I'm here to help you understand about ....."

# HELP
Help_statement = "You can talk to me in one of the following modes. \n" \
                 "/Quiz: To start a simple cognitive test \n" \
                 "/FAQ: Get answers to questions \n" \
                 "/Info: To give your information about learning disability \n" \
                 "/Help: See this message \n" \
                 "Typing: You can try typing in the textbox \n" \
                 "/start: To start all over again\n"

# Menu
Menu_statement = "Here is the Menu: \n" \
                 "/Quiz: To start a simple cognitive test \n" \
                 "/FAQ: Get answers to questions \n" \
                 "/Info: To give your information about learning disability \n"
# Statement
FAQ_statement = "Choose one of the questions from below to see the answer."

# Q1
FAQ_Q1 = "What kind of test does the chatbot use ?"

FAQ_Q2 = "All the data will be automatically deleted after 3 months."

#################################################################################

Info_statement = "Please the button below, choose which type of question you want to ask."

# Return to INFO MENU
RETURN_INFO_MENU = "Return to information menu: /INFO"

# About ADHD
ADHD_INFO_01 = "ADHD stands for Attention Deficit and/ Hyperactivity Disorder. \n" \
               "The precise causes have not yet been identified but research has demonstrated that ADHD has a very " \
               "strong neurobiological basis and is highly hereditary. The seriousness may depend on genetic make-up, " \
               "environmental conditions and stages in one’s life. "

# About ASD
ASD_INFO_01 = "Autism spectrum disorder (ASD) is a developmental disability  that can cause significant social, " \
              "communication and behavioral challenges. There is often nothing about how people with ASD look that " \
              "sets them apart from other people, but people with ASD may communicate, interact, behave, and learn in " \
              "ways that are different from most other people. The learning, thinking, and problem-solving abilities " \
              "of people with ASD can range from gifted to severely challenged. Some people with ASD need a lot of " \
              "help in their daily lives; others need less. "

ASD_INFO_02 = 'A diagnosis of ASD now includes several conditions that used to be diagnosed separately: autistic ' \
              'disorder, pervasive developmental disorder not otherwise specified (PDD-NOS), and Asperger syndrome. ' \
              'These conditions are now all called autism spectrum disorder. '

# About Learning Difficulties
LD_INFO_01 = "Learning disabilities are due to genetic and/or neurobiological factors that alter brain functioning in " \
             "a manner which affects one or more cognitive processes related to learning. These processing problems " \
             "can interfere with learning basic skills such as reading, writing and/or math.  They can also interfere " \
             "with higher level skills such as organization, time planning, abstract reasoning, long or short term " \
             "memory and attention.  It is important to realize that learning disabilities can affect an individual’s " \
             "life beyond academics and can impact relationships with family, friends and in the workplace. "

# More Information
MI_INFO_01 = "Click the below button to visit the website for getting more information."

MI_INFO_02 = "1. 衛生署兒童體能智力測驗服務 Child Assessment Service (DHCAS)\n" \
             "2. 專注力促進會 ADHD Foundation\n" \
             "3. Autism Spectrum Disorder (ASD) | Autism | NCBDDD | CDC"

# Store string for the test

# Forward number pattern question
INSTRUCTION_FORWARD_1 = "Now I am going to say some numbers.\n" \
                        "Listen carefully, and when I am through say them right after me"

INSTRUCTION_FORWARD_2 = "For example, if I say 9 2 7, you should say 927. \n" \
                        "Remember: please enter number only."

# Backward number pattern question

CONTENT_BACKWARD_1 = "Now I am going to say some more numbers but this time when I stop I want you to say them " \
                     "backwards. "

CONTENT_END = "That's the end of the test."

# common about message handle

Msg_01 = "Let's Start"
Msg_02 = "If you not agree the..... "

Back_To_Menu = "\\Menu"

# Agreement
Agreement_statement = "[The personal record will be kept in our database for 31 days and will then be erased " \
                      "automatically.\n Your Information will not use the in direct marketing, it only use on data " \
                      "analysis.The provision of the Data is voluntary. However, if you elect not to provide the Data " \
                      "to us, we may not be able to supply you with the relevant information or services or to " \
                      "process your request."

# GET user information
Cancel_getInfo = "If you want to end the test OR Stop giving information,\n" \
                 "Enter or Press  /cancel "

# confirm message
Check_info = 'Please confirm the information: \n'

# END
# Cancel : when get User information
restart_quiz = "If you want to start over again, \n" \
               "Click /quiz to start the quiz over again\n"

# invalid input message
incorrect_Name = "Please enter again: \n " \
                 "It's only allow Alphabet and Space\n" \
                 "A - Z / a - z / space"

incorrect_Age = "Please enter again: \n " \
                "It's only allow number (0-9)\n" \
                "And, the range need to within 6-99"

incorrect_dob = "Your input format or date is invalid.\n " \
                "Please enter again: \n" \
                "Format : 99-99-9999, dd-mm-yyyy"

incorrect_dob_2 = "Date of Birth cannot larger than today\n " \
                  "Please enter again: \n"

incorrect_dob_3 = "Invalid AGE is larger than 100\n " \
                  "Please enter again: \n"

incorrect_dob_4 = "Invalid AGE is smaller than 6\n " \
                  "Please enter again: \n"

incorrect_dob_5 = "Invalid AGE ! \n" \
                  "The age is different from your input age " \
                  "Please enter again: \n"

incorrect_gender = "Your input is invalid.\n " \
                   "Please enter again: \n" \
                   "Format : M OR F"

# Ready the test
Check_ready = "Let Start the test\n" \
              "ARE YOU READY ?'"

# Author
Who_Create = "This chatbot is created by Katrina Lau. \n" \
             "Student ID : 19001291S \n" \
             "Student Name : Lau Pui Kwan \n" \
             "IS Supervisor: Adam Wong"
