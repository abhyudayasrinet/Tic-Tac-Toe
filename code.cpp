#include<iostream>
#define BOT 1
#define HUM -1
#define DRAW 0
using namespace std;

struct matrix
{
    int mat[3][3];              // 3x3 board
    matrix()
    {
        for(int i=0;i<3;i++)
            for(int j=0;j<3;j++)
                mat[i][j]=0;
    }

};

//AI MOVE VALUE IS 3 AND HUMAN MOVE IS 5
void display(matrix m)
{
    for(int i=0;i<3;i++)
    {
        for(int j=0;j<3;j++)
        {
            if(m.mat[i][j]==5)
                cout<<'X'<<" ";
            else if(m.mat[i][j]==3)
                cout<<'O'<<" ";
            else
                cout<<'_'<<" ";
        }
        cout<<endl;
    }
    cout<<endl;
}

/*UPDATES THE MATRIX WITH THE HUMAN MOVE AS 5*/
int update(matrix &m,int n)
{
    for(int i=0,k=1;i<3;i++)
    {
        for(int j=0;j<3;j++,k++)
        {
            if(k==n && m.mat[i][j]!=0)
                return -1;                  //return value -1 in case the location is already occupied
            if(k==n && m.mat[i][j]==0)
                m.mat[i][j]=5;
        }
    }
    return 1;               //return value 1 for a successful move
}

/*CHECK FOR WIN/LOSE/DRAW
IF COLUMN/ROW/DIAGONAL SUM IS 15, THEN HUMAN WINS
IF COLUMN/SUM/DIAGONAL SUM IS 9,  THEN AI WINS*/
int win(matrix m)
{
    int s;
    //check rows
    for(int i=0;i<3;i++)
    {
        s=0;
        for(int j=0;j<3;j++)
        {
            s+=m.mat[i][j];
        }
        if(s==15)
            return HUM;
        else if(s==9)
            return BOT;
    }


    //check columns
    for(int j=0;j<3;j++)
    {
        s=0;
        for(int i=0;i<3;i++)
        {
            s+=m.mat[i][j];
        }
        if(s==15)
            return HUM;
        else if(s==9)
            return BOT;
    }

    //check main diagonal
    if(m.mat[0][0]+m.mat[1][1]+m.mat[2][2] == 15)
        return HUM;
    else if((m.mat[0][0]+m.mat[1][1]+m.mat[2][2] == 9))
        return BOT;

    //check other diagonal
    if(m.mat[0][2]+m.mat[1][1]+m.mat[2][0] == 15)
        return HUM;
    else if(m.mat[0][2]+m.mat[1][1]+m.mat[2][0] == 9)
        return BOT;

    //draw
    int flag=0;
    for(int i=0;i<3;i++)
    {
        for(int j=0;j<3;j++)
        {
            if(m.mat[i][j]==0)
                flag=1;
        }
    }
    if(flag)
        return -2;
    else
        return DRAW;
}


/*DECIDING THE NEXT MOVE / MINIMAX */
int next_move(matrix m,char turn)
{
    int k=win(m);
    int temp;

    if(k==BOT)
        return BOT;                 //RETURN VALUE BOT = 1 (BOT WINS)
    else if(k==HUM)
        return HUM;                 //RETURN VALUE HUM = -1 (HUMAN WINS)
    else if(k==DRAW)
        return DRAW;                //RETURN VALUE DRAW = 0 (DRAW)

    if(turn=='c')                   //IF AI's TURN
    {

        k=-99;                      //INITIALLY SET TO MIN FOR COMPARISON WITH FIRST BRANCH VALUE OF MAX NODE
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                if(m.mat[i][j]==0)
                {
                    m.mat[i][j]=3;
                    temp=next_move(m,'h');
                    if( temp > k)
                        k=temp;
                    m.mat[i][j]=0;
                }
            }
        }
    }
    else
    {
        k=99;                   //INITIALLY SET TO MAX FOR COMPARISON WITH FIRST BRANCH VALUE OF MIN NODE
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                if(m.mat[i][j]==0)
                {
                    m.mat[i][j]=5;
                    temp=next_move(m,'c');
                    if(temp < k)
                        k=temp;
                    m.mat[i][j]=0;
                }
            }
        }
    }

    return k;

}



int main()
{
    for(int i=0,k=1;i<3;i++)
    {
        for(int j=0;j<3;j++,k++)
        {
            cout<<k<<" ";
        }
        cout<<endl;
    }
    int n;
    matrix m,change;
    display(m);
    int k,temp;
    while(true)
    {
        cout<<"Enter your choice : ";
        cin>>n;
        if(update(m,n)==-1)
        {
            cout<<"Invalid move!!\n";
            continue;
        }

        if(win(m)==BOT)
        {
            display(m);
            cout<<" Computer Wins!\n" ;
            break;
        }
        else if( win(m)==HUM)
        {
            display(m);
            cout<<" You Win!!\n" ;
            break;
        }
        else if( win(m)==DRAW)
        {
            display(m);
            cout<<" DRAW!!\n";
            break;
        }

        k=-99;
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                if(m.mat[i][j]==0)
                {
                    m.mat[i][j]=3;              //CHOSE LOCATION FOR COMPUTER MOVE
                    temp=next_move(m,'h' );
                    if(temp>k)
                    {
                        k=temp;
                        change=m;               //STORE IF MOVE CHOSEN
                    }
                    m.mat[i][j]=0;              //RESET LOCATION
                }
            }
        }

        m=change;                              //APPLY BEST CHOSEN MOVE
        display(m);
        if(win(m)==BOT)
        {
            cout<<" Computer Wins!\n" ;
            break;
        }
        else if( win(m)==HUM)
        {
            cout<<" You Win!!\n" ;
            break;
        }
        else if( win(m)==DRAW)
        {
            cout<<" DRAW!!\n";
            break;
        }
    }
    return 0;
}


/*UNBEATABLE!*/

