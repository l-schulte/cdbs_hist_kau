from enum import Enum


class Metric(Enum):
    COMMENT_LINES = 'comment_lines'
    COMMENT_LINES_DENSITY = 'comment_lines_density'
    COMPLEXITY = 'complexity'
    CHURN = 'churn'
    NCLOC = 'ncloc'
    FUNCTIONS = 'functions'
    STATEMENTS = 'statements'
    DUPLICATED_LINES = 'duplicated_lines'
    VIOLATIONS = 'violations'
    CODE_SMELLS = 'code_smells'
    BUGS = 'bugs'
    VULNERABILITIES = 'vulnerabilities'
    SQALE_INDEX = 'sqale_index'
    SQALE_DEBT_RATIO = 'sqale_debt_ratio'
