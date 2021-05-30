# TKOM2021 - C++ do Python

#### Konrad Kulesza 300247



----

#### Podzbiór języka wejściowego

- typy danych:
  - int
  - string
  - bool
- komentarze - jedno- i wielolinijkowe
- zmienne lokalne
- operacje arytmetyczne
- wypisanie na ekran
  - z oraz bez znaku nowej linii
- wywołania funkcji
- instrukcje złożone:
  - if-else
  - while
- deklarowanie funkcji
  - argumenty
  - wartość zwracana

#### Założenia

- w kodzie dopuszczone są tylko znaki alfanumeryczne - w stringach dowolne
- wyrażenia zaczynające się znakiem `#` na przykład  `#include<iostream>` są przezroczyste, lekser nie przekazuje ich do dalszej analizy
- jeden plik na wejściu
- jeden plik na wyjściu
- nadpisywanie słów kluczowych języka wejściowego **nie** przerywa przetwarzania, ale użytkownik jest informowany, że kod wejściowy nie jest możliwy do skompilowania i wykonania.
- nadpisywanie słów kluczowych języka wyjściowego skutkuje przerwaniem przetwarzania.
- przypisanie wartości do zmiennej, która nie została wcześniej zadeklarowana **nie** przerywa przetwarzania, ale użytkownik jest informowany, że kod wejściowy nie jest wykonywalny.

#### Gramatyka

```
### komentarze
comment 			= <single_line_comment> | <multi_line_comment>
multi_line_comment 	= "/*" <string_char> "*/"
single_line_comment = "//" <string_char> <end_of_line>

### deklaracja funkcji
instruction_block	= {<simple_instruction> | <complex_instruction>}
scope				= "{" <instruction_block> "}"
function_body		= "{" <instruction_block> ["return" <right_value> ";"] "}"
function_declaration= <type> <identifier> "(" [<type><identifier>[{","<type> <identifier}]] ")""<function_body>


### instrukcje złożone
complex_instruction	= <if_statment> | <while_statement>
while_statement		= "while" "(" <condition> ")"  <scope>
if_statement		= "if" "(" <condition> ")" <scope> ["else"  <scope>]

### instrukcje proste
variable_declaration= <type> <identifier> [ "=" <right_value>]
variable_assignment = <identifier> "=" <right_value>
print_no_new_line	= <print_with_new_line> "<<" "std::endl"
print_with_new_line	= "std::cout" "<<" <right_value>
function_invocation = <identifier> "(" [<right_value> {"," <right_value>}]

simple_instruction 	= (<print_no_new_line> | <print_with_new_line> | <variable_assignment> | <variable_declaration> | <function_invocation> ) <end_of_ins>


### operacje arytmetyczne i warunki
aritmetic_operation = <arithmetic_component> <arithmetic_operand> <arithmetic_component>
aritmetic_component = ( "("<arithmetic_operation>")" ) | <literal> | <identifier>| <arithmetic_operation>
right_value			= <literal> | <aritmetic_operation> | <identifier>

condition 			= <comparison> | <literal> | <identifier>
comparison	 		= <comparison_operand> <comparison_operator> <comparison_operand>
comparison_operand 	= <literal> | <identifier>


### literały, typ i identyfikator
literal 			= <bool_literal> | <string_literal> | <integer_literal>
string_literal 		= <quote> char_string <quote>
bool_literal 		= "true" | "false"
integer_literal 	= <non_zero_digit> {digit}
char_string 		= (<special_char>| <char> | <end_of_ins>) {char_string}
type 				= "bool" | "int" | "std::string"
identifier			= {char}

###operatory
aritmetic_opeator 	= "+" | "-" | "*"
boolean_operator 	= "&&" | "||"
comparison_operator = "!=" | "==" | ">" | "<" | ">=" | "<="

###podstawowe
end_of_line 		= "\n"
end_of_ins 			= ";"
char 				= <digit> | <alphabet_char>
alphabet_char 		= [a-z] | [A-Z]
special_char 		= "!" | "@" | "#" | "%" | "^" | "&" ...
quote 				= <double_quote> | <single_quote>
double_quote 		= """
single_quote		= "'"
digit 				= "0"|<non_zero_digit>
non_zero_digit 		= "1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"

```



---

### Implementacja

#### Opis

TODO:

#### Struktury danych

- Token - typ tokenu, wartość, pozycja
- Symbole
  - zmiennych - nazwa oraz typ
  - funkcji - nazwa, typ wartości zwracanej, typy argumentów wejściowych
- AstNode - klasa bazowa węzła drzewa rozbioru, każdy element drzewa dziedziczy po niej

#### Widok z góry systemu - potok przetwarzania

<img src="E:\STUDIA\sem6\TKOM\projekt\tkom_2021\doc\dokumentacja_koncowa.assets\image-20210528173509781.png" alt="image-20210528173509781" style="zoom:100%;" />

#### Opis modułów

- Code Provider:
  - Odpowiedzialny za dostarczanie pojedynczych znaków kodu wejściowego do parsera oraz śledzenia miejsca w kodzie. 
  - Nie produkuję błędów.
- Lexer:
  - Składa dostarczone znaki w Tokeny. 
  - Pomija białe znaki. 
- Parser:
  - Składa dostarczone Tokeny w węzły drzewa składniowego.
- Semantic analyzer:
  - Przezroczysty w przypadku poprawnych struktur
  - Przepuszcza poprawne węzły AST
  - Konstruuję tablicę symboli oraz ją analizuje.
- Code Generator:
  - Tłumaczy otrzymane na wejściu drzewa AST na kod w języku Python. 
  - Uwzględnia odpowiednie wcięcia w zależności od poziomu zagnieżdżenia instrukcji.

#### Obsługa błędów

Rodzaje błędów:

- LekserError
- ParserError
- SemanticError
- DevelopmentError

#### We/Wy

Przykład wykonania programu: `./translate_file file.cpp`

Skutkiem wykonania jest plik o ten samej nazwie, ale rozszerzeniu `.py`, dla przykładu powyżej: `file.py`



Dodatkowo zdefiniowany jest skrypt `compare_outputs.sh`, który służy do porównania wyników wykonania kodu napisane w C++ oraz przetłumaczonego do Pythona. Jego schemat działania:

1. skompiluj kod .cpp
2. wykonaj skompilowany kod oraz zapisz jego wynik to pliku `cpp_output.txt`
3. wykonaj przetłumaczony plik .py oraz zapisz jego wynik do pliku `py_output.txt`
4. porównaj pliki, możliwe odpowiedzi:
   - `OK - files are the same`
   - `ERROR - files are NOT the same`
5. usuń pliki: wykonywalny oraz wyniki programów

#### Testy

- Lekser

  - Proste testy jednostkowe sprawdzające czy lekser rozpoznaje wszystkie rodzaje tokenów oraz sekwencje tokenów.

    Przykład, czy ciąg znaków `int a = 10;` zostanie odpowiednio przetłumaczony na tokeny `type=int, id=a, assign_operator, literal=10`

- Parser
  - Proste testy jednostkowe sprawdzające czy lekser z parserem komunikują się w odpowiedni sposób. W powyższym przykładzie parser powinien zwrócić węzeł AST=`VariableDeclaration` z podwęzłami `type=int`, `id=a` oraz `literal=10`

- Translator

  - Najbardziej złożone testy, ich przebieg jest następujący:

    1. Na wejściu zostaje podany kod programu w języku c++

    2. Zostaje zapisany plik źródłowy z podanym kodem

    3. Następuje analiza pliku wejściowego oraz translacja do kodu w języku Python

    4. Kod w języku c++ zostaje skompilowany

    5. Skompilowany kod zostaje wykonany, a jego wynik zostaje zapisany do pliku tekstowego

    6. Kod w języku Python także zostaje wykonany, a jego wynik zostaje zapisany do pliku tekstowego

    7. Oba pliki tekstowe zostają porównane, jeżeli się różnią to test zostaje zakończony porażką

    8. Wszystkie pliki wyprodukowane "po drodze" zostają usunięte

       Przykład - plik na wejściu:

       ```c++
       int main(){
       	int i = 0;
       	while(i<10){
       		std::cout<<i<<std::endl;
       		i = i+1;
       	}
       }
       ```

       po skompilowaniu i wykonaniu skutkuje wypisaniem na standardowe wejście cyfr od 0 do 10 włącznie, każda w nowej linijce. Kod po translacji do języka Python powinien zachowywać się tak samo. 



