from app.llm.prompt import ChatTemplate
from app.llm.memory import memory
from app.llm.llm_model import model

def llm_responce(query:str, db_info:str):
    temp = ChatTemplate()
    template = temp.template()
    # chat_history = memory.chat_memory.messages

    chain = template | model 
    result = chain.invoke({
        "user_query": query,
        "db_info": db_info
    })
    # memory.save_context({"HumanMessage": query}, {"AIMessage": result.content})
    return result.content


        # "chat_history": chat_history,