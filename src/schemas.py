from typing import List, Optional
from pydantic import BaseModel, Field

class LLMIntentPrediction(BaseModel):
    intent: str = Field(..., description="The predicted intent label from the taxonomy.")
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0.")
    reason: str = Field(..., description="Reasoning for the chosen intent.")

class ReplyGenerationResult(BaseModel):
    reply: str = Field(..., description="The generated support reply.")
    grounded: bool = Field(..., description="Whether the reply is grounded in historical evidence.")
    evidence_ids: List[str] = Field(default_factory=list, description="List of tweet IDs used as evidence.")

class EscalationDecision(BaseModel):
    decision: str = Field(..., description="Either 'AUTO_HANDLE' or 'ESCALATE'.")
    reason: str = Field(..., description="Reasoning for the escalation decision.")

class AgentResponse(BaseModel):
    intent: str
    confidence: float
    reply: str
    decision: str
    reason: str
    retrieved_examples: List[dict]

class JudgeEvaluation(BaseModel):
    groundedness: int = Field(..., ge=1, le=5)
    helpfulness: int = Field(..., ge=1, le=5)
    correctness: int = Field(..., ge=1, le=5)
    brand_tone: int = Field(..., ge=1, le=5)
    safety: int = Field(..., ge=1, le=5)
    rationale: str
