# TKOM_2021
## Zadanie "do Pythona"


Translator skrośny z C++ do Python



### Autor 

Konrad Kulesza 300247



## Dokumentacja wstępna

### Podzbiór języka C++

- komentarze
  - jednolinijkowe
  - wielolinijkowe
- zmienne dynamiczne
- typy danych:
  - int
  - string
  - float
  - boolean
- operacje arytmetyczne(zmiennopozycyjne, stałopozycyjne)
- wypisanie na ekran
- instrukcje złożone
  - if, else
  - for
  - while
- funkcje

#### Założenia

wejście: kompilowalny jeden plik .cpp

### We/wy

Program będzie wywoływany z argumentem wejściowym z nazwą pliku do przetłumaczenia, np:`./translator nazwa_pliku.cpp`

W tym samym folderze zostanie utworzony przetłumaczony plik źródłowy w języku python `nazwa_pliku.py`



Dodatkowo, na standardowe wyjście wypisywane będą komunikaty o błędach oraz ostrzeżeniach.

### Testowanie

Do każdego modułu zostaną napisane odpowiednie testy jednostkowe(np. czy lekser odpowiednio rozpoznaje tokeny).

Zostanie także przetestowana komunikacja pomiedzy modułami sąsiadującymi.

Zostaną także napisane testy funkcjonalne całego translatora.

Dodatkowo, pojawią się też testy polegające na porównaniu wyników kodu wejściowego i wyjściowego.

#### Przykładowe konstrukcje / testy funkcjonalne

```
int a = 5;
int b = 10;
double c = 100.00;
double result = (a+b)*c/20;
-----
a = 5
b = 10
c = 100.00
result = (a+b)*c/20
```

```
bool cond = true;
int a = 15;
if(a<15){
	a=a+2;
}else if(cond){
	a=a-2;
}
-----
cond = true
a = 15
if a<15:
	a=a+2
elif cond:
	a=a-2
```

```
for(int i=0; i<10; i=i+1){
	std::cout<<i<<std::endl;
}
-----
for i in range(0, 10):
	print(i)
```

```while()
int main(){
	int i=0;
	while( i<10 ){
		++i;
	}
}
-----
def main():
	i=0
	while i<20:
		++i
```

```
void fun(int a){
	a = a + 2;
	/*
	komentarz wielolinijkowy
	*/
	std::cout<<a;
	
}
-----
def fun(a: int){
	a=a+2
	'''
	komentarz wielolinijkowy
	'''
	print(a)
}
```



### Obsługa błędów

Błędy będą dzielone na dwa rodzaje:

- krytyczne - plik wynikowy nie zostaje utworzony
- niekrytyczne - ostrzeżenia; wysyłają komunikat, ale przetwarzanie pliku jest kontynuowane 



Błędy będą wypisywane na standardowe wyjście.



Komunikat błędu(ostrzeżenia) będzie posiadał:

- rodzaj błędu
- miejsce wystąpienia błędu; linijka, kolumna
- opis błędu( np. na którym etapie )



##### Przykładowe błędy:

```
for( i a b ); // Error! Line: 6, column: 1; Syntax error: for_statment
```

```
else if{} // Error! Line: 11, column 1; Syntax error: if_else_statment
```

```
class = 5; // Error! Line: 11, column 1; Keyword violation
```

```
0abc = 2; // Error! Line: 11, column 1; Variable name error
```

```
// int a=1;
a = 3; // Error! Line: 11, column 1; Variable is undefined!
```





### Opis realizacji modułów

#### Lekser

Ślezdenie linii i kolumny, rozpoznawanie tokenów i przekazywanie ich do parsera. Pomijanie nadmiarowych białych znaków.

#### Parser

Tworzenie drzewa składniowego. Analiza od lewej do prawej.  Rekursja lewostronnie zstępująca. Walidacja składni. Zapisywanie odpowiednich tokenów do talbicy symboli.

#### Analizator semantyczny

Sprawdzanie czy struktury mają sens w kontekście języka. Sprawdzanie typów.

### Składnia

```

comment				= <single_line_comment> | <multi_line_comment>
multi_line_comment	= "/*" <string_char> "*/"
single_line_comment	= "//" <string_char> <end_of_line>

print				= <print_without_nl> | <print_with_nl>
statment			= <if_statment> | <for_statment> | <while_statement>

print_with_nl		= <start_print> "std::endl" <end_of_ins>
print_without_nl	= <start_print> <enf_of_ins>
start_print			= "std::cout<<" ( <variable_name> | <literal> | <condition> )
while_statement		= "while" "(" <complex_condition> ")" <scope>
for_statment		= "for" "(" <variable_declaration> ";" <complex_condition> ";" <instruction> ")" <scope>
if_statment			= "if" "(" <complex_condition> ")" <scope> [ "else" <scope>]


right_value			= <literal> | <aritmetic_operation> | <variable_name>


aritmetic_operation	= <arithmetic_component> <arithmetic_operand> <arithmetic_component>
aritmetic_component	= ( "("<arithmetic_operation>")" ) |<literal>|<variable_name>| <arithmetic_operation>

function_scope		= <start_of_scope> [<return> [<right_value>] <end_of_ins>] "}"
scope				= <start_of_scope>  "}"
start_of_scope		= "{" <instruction_block>

instruction_block	= single_instruction {instruction_block}
single_instruction	= <variable_declaration> | <variable_assignment> | <statment> | <print>

complex_condition	= <single_condition> | <complex_condition> [ <boolean_operator> <complex_condition>]
single_condition	= <literal> | <comparision>
comparision			= <comparison_operand> <comparison_operator> <comparison_operand>
comparison_operand	= <variable_name> | <literal>

variable_declaration= <type> <variable_assignment>
function_declaration= <type> <variable_name> "(" [<type><variable_name>][{","<type> <variable_name}] ")"<scope>
variable_assignment	= <variable_name> "=" <right_value> <end_of_ins>

type 				= "int" | "bool" | "float" | "string"

variable_name		= <start_of_var> , [char]
start_of_var 		= <alphabet_char> | "_"

literal				= <bool_literal> | <float_literal> | <string_literal> | <integer_literal>

string_literal		= <cudzysłow> char_string <cudzysłów>
bool_literal		= "true" | "false"
float_literal		= {digit} "." {digit}
integer_literal		= <non_zero_digit> {digit}

char_string			= (<digit> | <special_char> | <alphabet_char> | <char> | <end_of_ins>) {char_string}

aritmetic_opeator	= "+" | "/" | "-" | "*"
boolean_operator	= "&&" | "||"
comparison_operator = "!=" | "==" | ">" | "<" | ">=" | "<=" 

end_of_line			= "\n" //zastanowić się
end_of_ins			= ";"
char 				= <digit> | <alphabet_char>
alphabet_char 		= [a-z] | [A-Z]
special_char		= "!" | "@" | "#" | "%" | "^" | "&" ...

digit				= "0"|<non_zero_digit>
non_zero_digit 		= "1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"

```



#### Wstępny-hasłowy pomysł na implementację

- Klasy/struktury danych
  - Token
  - Statment
    - if, else
    - while
    - for
  - Function
    - typ wartości zwracanej
    - lista argumentów
  - Variable
    - typ danych
  - bufor tymczasowy
  - stos zmiennych
    - globalny
    - lokalny



- wstępny algorytm generowania kodu

1. pobieraj znaki aż do rozpoznania tokenu
   - czy token występuje w podzbiorze języka?
2. dopasuj do kontekstu
   - czy tworzy strukture?
   - jeżeli deklaracja zmiennej/funkcji - czy nie nadpisuje słowa kluczowego?
   - jeżeli przypisane - czy zmienna jest w dostępna w danym bloku?
3. sprawdź poprawność
   - czy typy zmiennych się zgadzają?
4. przetłumacz struktury języka c++ na odpowiadające im struktury w języku Python



#### Dodatkowe

Nie można pozwolić żeby nazwy funkcji/zmiennych "nadpisywały" słowa kluczowe któregokolwiek z języków

``` 
cpp_keywords = if, else, while, for, class, int, long, double, true, false, ...
python_keywords = if, elif, else, while, for, in, range, class, def, True, False, ...
```

  