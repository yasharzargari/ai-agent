from ...core.language import Goal

SYNTHESIZER_GOALS = [
    Goal(
        priority=1,
        name="Deduplicate Information",
        description="""
        Remove duplicate or highly similar information:
        - Identify duplicate content across sources
        - Keep the most authoritative or complete version
        - Note when information conflicts across sources
        """
    ),
    Goal(
        priority=2,
        name="Cluster by Topic",
        description="""
        Group related information together:
        - Identify main topics or themes
        - Cluster information by topic/ticket/category
        - Maintain source attribution for each cluster
        """
    ),
    Goal(
        priority=3,
        name="Generate Summary",
        description="""
        Create a comprehensive summary report:
        - Write clear, structured summary of findings
        - Include bullet points for key information per source
        - Highlight important patterns or insights
        - Use proper formatting and attribution
        Return the final report using return_synthesis_result.
        """
    )
]
