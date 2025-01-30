from flask import Flask, render_template, request, jsonify, make_response
from openai import OpenAI
import threading
import time
import re
import os 
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Replace with your OpenAI API key
# Set your OpenAI API key
client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
conversation_history = []
bot_1_prompt = ""
bot_2_prompt = ""
is_running = False
status_message = "Waiting for agents to start"

LINK_HEALTH_PROMPT = """
Background: Link Health      Link Health: Addressing Social Determinants of Health Through Innovation and Impact
1. Introduction to Link Health
Link Health is a pioneering organization dedicated to bridging the gap between healthcare and social services by connecting vulnerable individuals and families to underutilized federal and state aid programs. Recognizing that social determinants of health (SDOH) significantly impact health outcomes, Link Health employs a unique blend of human connection and cutting-edge technology to create a scalable and sustainable model that empowers individuals while reducing healthcare costs.
Mission Statement:
Link Healths mission is to ensure that no eligible individual misses out on the benefits they need to live healthier, more secure lives. By focusing on maximizing the utilization of available federal and state funds, Link Health aims to transform these resources into tangible support for those experiencing food insecurity, housing instability, utility challenges, and other critical needs.
Origins and Growth:
Link Health originated as a pilot program within the Emergency Department (ED) of Massachusetts General Hospital. Recognizing the significant downtime patients experienced while waiting for care, the program offered immediate access to information and enrollment assistance for federal benefit programs. This innovative approach transformed a traditionally overlooked opportunity into a crucial lifeline for vulnerable populations.
The pilot program quickly demonstrated the immense potential of this model, successfully securing over $415,000 in federal benefits for participants within a short period. This success propelled Link Healths expansion city-wide in Boston, with funding from Mayor Michelle Wus administration and the City of Bostons Digital Equity Fund. Subsequent state funding and approval enabled statewide scaling across Massachusetts. Building on this momentum, Link Health has expanded its reach into Texas and has now facilitated the distribution of over $3 million in benefits, including WIC, SNAP, cash assistance, the Earned Income Tax Credit (EITC), and other crucial programs. This expansion highlights Link Healths ability to adapt its model to diverse regions and address the unique needs of individuals in different states.
Key Programs and Impact:
Link Health focuses on connecting individuals with a range of federal and state programs, including:
SNAP (Supplemental Nutrition Assistance Program): Combating food insecurity.
WIC (Women, Infants, and Children): Supporting the nutritional health of pregnant women, new mothers, and young children.
LIHEAP (Low-Income Home Energy Assistance Program): Assisting families with home heating and cooling costs.
Lifeline Program: Providing discounted communication services.
EITC (Earned Income Tax Credit): Offering financial relief for low-to-moderate-income working families.
Transitional Aid to Families with Dependent Children (TAFDC): Offering temporary cash assistance to families with dependent children.
Child Care Financial Assistance (CCFA): Helping families afford childcare.
Medicare Savings Program: Helps people with Medicare pay for Medicare costs.
Affordable Connectivity Program (ACP): Provides discounts for internet service for eligible households.
By addressing these fundamental needs, Link Health empowers individuals to focus on their health and well-being. The organizations work not only improves individual lives but also reduces systemic pressures on the healthcare system, such as emergency department overutilization and hospital readmissions.
Why Link Health Matters:
The connection between SDOH and health outcomes is well-established. Factors such as housing, nutrition, financial stability, and access to communication services account for a significant portion of an individuals overall health. Traditional healthcare models often overlook these crucial factors. Link Health directly addresses this gap by providing immediate interventions that deliver both short-term relief and long-term benefits.
Link Health has demonstrated its ability to drive systemic change. By facilitating the distribution of over $3 million to vulnerable families in Massachusetts and Texas, the organization is setting a new standard for addressing unmet social needs at scale. In a healthcare landscape increasingly focused on value-based care, Link Health offers a practical and impactful solution that effectively integrates social services and health systems to redefine patient-centered care.
2. How Link Health Operates
Link Healths success is rooted in its innovative approach, which seamlessly integrates human connection with advanced technology to create a truly patient-centered model.
Patient Engagement Process:
Link Health meets individuals where they are, both physically and emotionally. The organization operates within healthcare settings, such as ED waiting rooms, community health centers, and through community outreach, where individuals often experience extended wait times and heightened stress. These settings provide opportunities for Link Healths certified patient navigators to engage individuals in a trusted and supportive manner. Link Health also utilizes text messaging and other digital tools to engage and enroll individuals in benefits remotely, increasing accessibility and efficiency.
Link Health has made significant strides in connecting individuals with essential benefits. To date, the organization has screened over 17,055 individuals for various benefit programs, enrolled 2,447 people, and facilitated the distribution of over $2,047,161 in federal and state benefits. Notably, 41% of those served are over 50 years old.
Key components of the patient engagement process include:
Needs Identification: Patient navigators initiate conversations to identify immediate social needs, such as food insecurity, housing instability, utility challenges, and access to communication services. Through focused interactions, navigators assess eligibility for various federal and state benefit programs.
Enrollment Assistance: Navigators guide individuals through the often-complex enrollment process for programs like SNAP, WIC, LIHEAP, cash assistance, EITC, and others. Applications are often completed on-site or remotely, ensuring immediate action and minimizing burden on individuals.
Ongoing Support: Individuals receive follow-up communication to address any questions or obstacles, ensuring they successfully access the benefits for which they have applied.
Human + AI Hybrid Model:
A key differentiator of Link Health is its innovative hybrid model, which combines the empathy and expertise of human navigators with the efficiency and scalability of artificial intelligence (AI).
Role of Patient Navigators: Patient navigators serve as trusted messengers, building rapport with individuals and providing empathetic, culturally sensitive support.
Integration of AI: AI systems automate repetitive tasks, such as verifying eligibility, submitting applications, and tracking enrollment progress. This automation ensures accuracy, speed, and reduces administrative burden.
Efficiency and Burnout Prevention: By automating routine tasks, Link Health reduces burnout among navigators, allowing them to focus on high-impact, patient-facing activities.
3. Addressing Social Determinants of Health (SDOH)
Social Needs Screening:
Link Healths navigators conduct screenings to assess critical social needs, including food insecurity, housing instability, utility challenges, and access to communication services. These screenings provide valuable insights into the specific challenges faced by individuals and inform appropriate interventions.
Federal and State Programs: Turning Resources into Impact:
Link Health connects individuals with a range of federal and state programs, including SNAP, WIC, LIHEAP, Lifeline, EITC, TAFDC, CCFA, Medicare Savings Program, and ACP. The organization has facilitated the distribution of over $3 million in benefits in Massachusetts and Texas, demonstrating the real-world impact of its work.
Improving Health Outcomes:
Link Healths interventions lead to improved health outcomes for individuals, healthcare systems, and communities:
For Individuals: Improved chronic disease management, reduced stress, and enhanced overall well-being.
For Healthcare Systems: Lower ED utilization, reduced hospital readmissions, and significant cost savings.
For Communities: Increased economic stability through the reinvestment of federal and state funds.
Broader Implications:
Link Healths work has broader implications for health equity, systemic change, and scalability:
Health Equity: Closing health disparities for vulnerable populations.
Systemic Change: Advocating for policy changes and increased investments in social services.
Scalability: Expanding the model to other states and healthcare systems.
Recent Developments:
Expansion into Texas: Link Health has successfully expanded its operations into Texas, facilitating the distribution of over $3 million in benefits.
New Contract Negotiations: Link Health is currently negotiating a contract with NeighborHealth System, an Accountable Care Organization (ACO) in Massachusetts, to directly bill Medicaid for its services through reimbursements.
University Partnerships: Link Health has partnered with 10 universities across Massachusetts and Texas to provide students with real-world experience as certified patient navigators. These students provide 10-12 hours per week of direct service, creating a scalable staffing model for both on-site and remote operations.
"""

# Function to interact with GPT-4
def gpt4_response(bot_prompt, user_message):
    messages = [
        {"role": "system", "content": bot_prompt},
        {"role": "user", "content": user_message}
    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
        max_tokens=1000,
        frequency_penalty=0.0
    )

    response_text = response.choices[0].message.content
    tokens_used = response.usage.total_tokens

    return {"response": response_text, "tokens_used": tokens_used}

def agent_conversation(prompt1, prompt2, MAX_ITERATIONS):
    global conversation_history, is_running, status_message

    agent1_response = gpt4_response(prompt1, prompt1)["response"]
    agent2_response = gpt4_response(prompt2, agent1_response)["response"]

    conversation_history = [
        {"content": agent1_response, "agent": "agent1"},
        {"content": agent2_response, "agent": "agent2"}
    ]

    iteration = 1  # Already performed the first cycle

    while iteration < MAX_ITERATIONS and is_running:
        time.sleep(2)  # Simulate delay

        try:
            status_message = "Agent 1 is thinking"
            agent2_last_response = conversation_history[-1]["content"]
            agent1_response = gpt4_response(prompt1, agent2_last_response)["response"]
            conversation_history.append({"content": agent1_response, "agent": "agent1"})

            status_message = "Agent 2 is thinking"
            agent2_response = gpt4_response(prompt2, agent1_response)["response"]
            conversation_history.append({"content": agent2_response, "agent": "agent2"})

            iteration += 1
            print("current iteration is", iteration)
        except Exception as e:
            is_running = False
            break

    is_running = False  # Stop conversation after MAX_ITERATIONS
    status_message = "The agents have concluded their work."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_agents():
    global conversation_history, is_running, status_message
    data = request.json
    prompt1 = data["prompt1"] + LINK_HEALTH_PROMPT
    prompt2 = data["prompt2"] + LINK_HEALTH_PROMPT
    MAX_ITERATIONS = data["maxIterations"]

    is_running = True
    status_message = "Agents are starting"
    conversation_thread = threading.Thread(target=agent_conversation, args=(prompt1, prompt2, MAX_ITERATIONS))
    conversation_thread.start()

    return jsonify({"status": "started"})

@app.route("/get_conversation", methods=["GET"])
def get_conversation():
    return jsonify({
        "history": conversation_history,
        "status": status_message,
        "final_idea": conversation_history[-2]["content"] if len(conversation_history) > 1 else ""
    })

@app.route("/stop", methods=["POST"])
def stop_conversation():
    global is_running
    is_running = False
    status_message = "The agents have concluded their work."
    return jsonify({"message": "Conversation stopped"})

@app.route('/download_transcript', methods=['GET'])
def download_transcript():
    transcript = "\n".join([f"{msg['agent']}: {msg['content']}" for msg in conversation_history])
    response = make_response(transcript)
    response.headers["Content-Disposition"] = "attachment; filename=conversation_transcript.txt"
    response.headers["Content-Type"] = "text/plain"
    return response

def extract_score(agent2_response):
    """Extracts the final overall score from Agent 2's response."""
    match = re.search(r"Overall Score: \s*(\d+(\.\d+)?)", agent2_response)
    return float(match.group(1)) if match else "Unknown"

@app.route("/status")
def get_status():
    global conversation_history

    last_idea = "No idea yet."
    last_score = "Waiting for score..."

    if len(conversation_history) >= 2:
        last_idea = conversation_history[-2]["content"]
        last_score = extract_score(conversation_history[-1]["content"])

    return jsonify({
        "latest_idea": last_idea,
        "latest_score": last_score
    })

if __name__ == "__main__":
    app.run(debug=True)
