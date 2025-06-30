import ply.lex as lex
import ply.yacc as yacc

### LEXER

tokens = (
    'VAR',
    'CONJUNCTION', 'DISJUNCTION', 'IMPLICATION', 'NEGATION',
    'LPAREN', 'RPAREN'
)

t_VAR = r'[a-z]'
t_CONJUNCTION = r'/\\'
t_DISJUNCTION = r'\\/'
t_IMPLICATION = r'->'
t_NEGATION = r'~'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

### PARSER

def p_expression_conjunction(p):
    'expression : expression CONJUNCTION expression'
    p[0] = p[1] + p[3]

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_clause(p):
    'expression : clause'
    p[0] = [p[1]]

def p_clause_implication(p):
    'clause : literal IMPLICATION literal'
    if p[1].startswith('~'):
        p[0] = [p[1][1:], p[3]]
    else:
        p[0] = ['~' + p[1], p[3]]

def p_clause_disjunction(p):
    'clause : literal DISJUNCTION literal'
    p[0] = [p[1], p[3]]

def p_clause_unit(p):
    'clause : literal'
    p[0] = [p[1]]

def p_literal_negation(p):
    'literal : NEGATION literal'
    p[0] = '~' + p[2]

def p_literal_var(p):
    'literal : VAR'
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

### UTILITY

def is_tautology(clause):
    return any(f"~{lit}" in clause for lit in clause)

def has_duplicate_literals(clause):
    return len(set(clause)) < len(clause)

def resolve(clause1, clause2):
    for lit in clause1:
        if f"~{lit}" in clause2:
            new_clause = list(set([x for x in clause1 if x != lit] + [x for x in clause2 if x != f"~{lit}"]))
            return new_clause
        if lit.startswith('~') and lit[1:] in clause2:
            new_clause = list(set([x for x in clause1 if x != lit] + [x for x in clause2 if x != lit[1:]]))
            return new_clause
    return None

### SATISFIABILITY

def is_satisfiable(cnf, trace=True):
    clauses = parser.parse(cnf)
    clauses = [c for c in clauses if not is_tautology(c) and not has_duplicate_literals(c)]
    seen = set(tuple(sorted(c)) for c in clauses)
    steps = []

    while True:
        new_clause_added = False
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                c1, c2 = clauses[i], clauses[j]
                resolvent = resolve(c1, c2)
                if resolvent:
                    resolvent_key = tuple(sorted(resolvent))
                    if resolvent_key not in seen and not is_tautology(resolvent):
                        seen.add(resolvent_key)
                        clauses.append(resolvent)
                        steps.append((c1, c2, resolvent))
                        new_clause_added = True
                        if resolvent == []:
                            if trace:
                                print("\nResolution Trace (UNSAT):")
                                for s in steps:
                                    print(f"{s[0]} ∧ {s[1]} ⟶ {s[2]}")
                            return False
        if not new_clause_added:
            if trace:
                print("\nResolution Trace (SAT):")
                for s in steps:
                    print(f"{s[0]} ∧ {s[1]} ⟶ {s[2]}")
            return True, clauses

### ASSIGNMENT

def sat_assignment(cnf):
    result = is_satisfiable(cnf, trace=False)
    if result is False:
        return None
    _, resolution_clauses = result
    clauses = parser.parse(cnf)
    variables = {lit.strip('~') for clause in clauses for lit in clause}
    assignment = {var: False for var in variables}

    for clause in resolution_clauses:
        for lit in clause:
            var = lit.strip('~')
            assignment[var] = not lit.startswith('~')

    # Final validation
    for clause in clauses:
        if not any((lit.startswith('~') and not assignment[lit[1:]]) or
                   (not lit.startswith('~') and assignment[lit]) for lit in clause):
            return None
    return assignment
