from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel


class RuleDisable(BaseModel):
    rule_id: str
    reason_for_disabling: str
    length_of_time: str


class RuleDisableResponse(BaseModel):
    previous_level: Optional[str]
    message: str
    success: bool


class RuleEnable(BaseModel):
    rule_id: str
    reason_for_enabling: str


class RuleEnableResponse(BaseModel):
    new_level: Optional[str]
    message: str
    success: bool


class AllDisabledRule(BaseModel):
    rule_id: str
    previous_level: str
    new_level: str
    reason_for_disabling: str
    length_of_time: str
    disabled_by: str


class AllDisabledRuleResponse(BaseModel):
    disabled_rules: List[AllDisabledRule]
    success: bool
    message: str
