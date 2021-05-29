#include<string>
#include<iostream>

std::string strFun(int a){
    std::cout<<"strFun";
    return "strFunReturn";
}

int main(){

    strFun(1);

}