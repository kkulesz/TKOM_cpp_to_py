#include<string>
#include<iostream>

int fun(int arg1, int arg2){
    int i = -10;
    while( i > 0 ){
        std::cout<<i<<std::endl;
        std::cout<<"\n";
        i = i-1;
        int a = (i-2) * (-3);
    }

    return -12;
}

int main(){
    fun(1,2);
    return 0 ;
}

