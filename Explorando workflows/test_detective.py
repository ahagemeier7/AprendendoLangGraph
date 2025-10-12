from detective_history import detective_workflow

def test_detective_story():
  result = detective_workflow.invoke({})
  
  print("\n=== História do detetive ===\n")
  
  print("\n === Primeiro Ato === \n")
  print(result["story"]["act_1"])
  print("\n === Segundo Ato === \n")
  print(result["story"]["act_2"])
  print("\n === Terceiro Ato === \n")
  print(result["story"]["act_3"])
  print("\n === Quarto Ato === \n")
  print(result["story"]["act_4"])
  
  print("\n === Elementos da história ===\n")
  
  print(f"Detetive: {result['detective']}")
  print(f"Crime: {result['crime']}")
  print(f"local: {result['location']}")
  print(f"clue: {result['clue']}")
  
if __name__ == "__main__":
  test_detective_story()