#include<string>
#include<iostream>

std::string strFun(int a){
    std::cout<<"strFun"<<std::endl;
    return "strFunReturn";
}

int main(){
    int i = 0;
    while( i<10 ){
        std::cout<<i<<std::endl;
        strFun("");
        i = i + 1;
    }
    int asd = 12;
    std::cout<<123<<std::endl;
    std::cout<<"nananana"<<std::endl;
}