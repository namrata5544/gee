from utils.groq_llm import get_llm

def summarize_findings(trend_result):
    prompt = f"""
    Based on this result: {trend_result}, write a short summary for a report.
    """
    result = get_llm().invoke(prompt).content
    with open("output/analysis_summary.txt", "w") as f:
        f.write(result)
    return result
