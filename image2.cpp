#include<iostream>
using namespace std;

int main() {
	int x = 0;
	int y = 0;
	int n = 0;
	cout << "请输入x的值：";
	cin >> x ;
	cout << "请输入y的值：";
	cin >> y ;
	cout << "请输入n的值：";
	cin >> n ;
	int** image = new int*[n]; // 创建行数为n的指针数组,表示包含n个int*指针的一个数组，每一个int*又指向包含n个整数的数组
	for (int i = 0; i < n; ++i){
		image[i] = new int[n]; // 为每一行开辟n列空间，表示包含n个整数的一个数组，这里的 image[i] 就相当于上面的 int*
		for (int j = 0; j < n; ++j){
			if (i == j) {
				image[i][j] = y;
			}
			else{
				image[i][j] = x;
			}
			cout << image[i][j];
		}
		cout << endl;
	}
	for (int i = 0; i < n; ++i) {
		delete[] image[i]; //释放每一行整数数组的内存,释放数组空间使用 delete[],释放单个对象空时使用delete
		image[i] = nullptr;
	}
	delete[] image; //释放行指针数组的内存
	image = nullptr;
	return 0;
}