#include<iostream>
using namespace std;

int main() {
	int x = 0;
	int y = 0;
	int n = 0;
	cout << "������x��ֵ��";
	cin >> x ;
	cout << "������y��ֵ��";
	cin >> y ;
	cout << "������n��ֵ��";
	cin >> n ;
	int** image = new int*[n]; // ��������Ϊn��ָ������,��ʾ����n��int*ָ���һ�����飬ÿһ��int*��ָ�����n������������
	for (int i = 0; i < n; ++i){
		image[i] = new int[n]; // Ϊÿһ�п���n�пռ䣬��ʾ����n��������һ�����飬����� image[i] ���൱������� int*
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
		delete[] image[i]; //�ͷ�ÿһ������������ڴ�,�ͷ�����ռ�ʹ�� delete[],�ͷŵ��������ʱʹ��delete
		image[i] = nullptr;
	}
	delete[] image; //�ͷ���ָ��������ڴ�
	image = nullptr;
	return 0;
}