# TKOM_2021
## Zadanie "do Pythona"


Translator skrośny z C++ do Python





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

### We/wy

Program będzie wywoływany z argumentem wejściowym z nazwą pliku do przetłumaczenia, np:`./translator nazwa_pliku.cpp`

W tym samym folderze zostanie utworzony przetłumaczony plik źródłowy w języku python `nazwa_pliku.py`



Dodatkowo, na standardowe wyjście wypisywane będą komunikaty o błędach oraz ostrzeżeniach

### Testowanie

Do każdego modułu zostaną napisane odpowiednie testy jednostkowe(np. czy lekser odpowiednio rozpoznaje tokeny).

Zostanie także przetestowana komunikacja pomiedzy modułami sąsiadującymi.

Zostaną także napisane testy funkcjonalne całego translatora.

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
- opis błędu



##### Przykładowe błędy:

```
for( i a b ); // Error! Line: 6, column: 1; Syntax error: for_statment
```

```
else if{} // Error! Line: 11, column 1; Syntax error: if_else_statment
```

```
class = 5; // Error! ----- Keyword violation
```

```
0abc = 2; // Error! ------ Variable name error
```

```
// int a=1;
a = 3; // Error! ------ Variable is undefined!
```





### Opis realizacji modułów

#### Lekser

Ślezdenie linii i kolumny, rozpoznawanie tokenów i przekazywanie ich do parsera.

#### Parser

Analiza od lewej do prawej.  Rekursja lewostronnie zstępująca.

#### Analizator semantyczny

Sprawdzanie czy struktury mają sens w kontekście języka.

#### Struktury danych

- bufor tymczasowy
- stos zmiennych
  - globalny
  - lokalny

#### Składnia

```
... do dokonczenia...
for_statment		= "for" "(" <variable_declaration> ";" <condition> ";" <instruction> ")" ...
if_statment			= "if" "(" <condition> ")" <instruction>|( "{"<instruction_block>"}")
variable_declaration= <type> <variable_name> ["=" ...]
function_declaration= <type> <variable_name> "(" [<type><variable_name>][{","<type> <variable_name}]")" "{" <instruction_block> "}"
type 				= "int" | "bool" | "float" | "string"
aritmetic_opeator	= "+" | "/" | "-" | "*"
boolean_operator	= "&&" | "||"
comparison_operator = "!=" | "==" | ">" | "<" | ">=" | "<=" 
variable_name		= <start_of_var> , [char]
start_of_var 		= <alphabet_char> | "_"
char 				= <digit> | <alphabet_char>
alphabet_char 		= [a-z] | [A-Z]
digit				= "0"|<non_zero_digit>
non_zero_digit 		= "1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"

```



#### Dodatkowe

Nie można pozwolić żeby nazwy funkcji/zmiennych "nadpisywały" słowa kluczowe któregokolwiek z języków/języka docelowego

``` 
cpp_keywords = if, else, while, for, class, int, long, double, true, false, ...
python_keywords = if, elif, else, while, for, in, range, class, def, True, False, ...
```

  