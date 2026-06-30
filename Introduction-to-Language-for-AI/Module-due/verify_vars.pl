% 1. BASE CASE: An empty list of records yields an empty list of passed subjects.
passed_exams([], []).

% 2. RECURSIVE CASE 1: The student took the exam and passed (Grade >= 18).
% We add the Subject to the result list.
passed_exams([exam(Subject, Grade) | Tail], [Subject | PassedTail]) :-
    Grade >= 18,                     
    passed_exams(Tail, PassedTail).

% 3. RECURSIVE CASE 2: The student took the exam but failed (Grade < 18).
% We DO NOT add the Subject to the result list.
% By explicitly stating Grade < 18, this rule cannot possibly overlap with Case 1.
passed_exams([exam(_, Grade) | Tail], PassedTail) :-
    Grade < 18,                      
    passed_exams(Tail, PassedTail).

% 4. RECURSIVE CASE 3: The record is a placeholder (like 'absent').
% We DO NOT add anything to the result list.
% We use \= (not unifiable) to ensure this only catches things that aren't exams,
% preventing this rule from accidentally swallowing valid exams.
passed_exams([Record | Tail], PassedTail) :-
    Record \= exam(_, _),            
    passed_exams(Tail, PassedTail).
