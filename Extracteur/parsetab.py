
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = '524A182CE4EBF87CAA8568C2439C42A2'
    
_lr_action_items = {'(':([0,1,7,8,10,11,13,],[1,3,-8,3,-2,-3,3,]),'$end':([2,9,],[0,-1,]),'MOT':([3,7,8,],[7,-8,15,]),')':([4,5,6,10,11,12,13,14,15,16,],[9,10,11,-2,-3,-7,-6,-4,-9,-5,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'Sprim':([0,],[2,]),'syntagme':([3,],[5,]),'lexique':([3,],[6,]),'leaf':([8,],[12,]),'S':([1,8,13,],[4,13,13,]),'exprs':([8,13,],[14,16,]),'head':([3,],[8,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> Sprim","S'",1,None,None,None),
  ('Sprim -> ( S )','Sprim',3,'p_axiome','ParserSyntaxer.py',22),
  ('S -> ( syntagme )','S',3,'p_S_1','ParserSyntaxer.py',26),
  ('S -> ( lexique )','S',3,'p_S_2','ParserSyntaxer.py',31),
  ('syntagme -> head exprs','syntagme',2,'p_syntagme','ParserSyntaxer.py',36),
  ('exprs -> S exprs','exprs',2,'p_exprs','ParserSyntaxer.py',42),
  ('exprs -> S','exprs',1,'p_exprs','ParserSyntaxer.py',43),
  ('lexique -> head leaf','lexique',2,'p_lexique','ParserSyntaxer.py',52),
  ('head -> MOT','head',1,'p_head','ParserSyntaxer.py',58),
  ('leaf -> MOT','leaf',1,'p_leaf','ParserSyntaxer.py',64),
]
