package hk.edu.polyu.comp.comp2021.simple.model;

import org.junit.Test;

import java.util.Scanner;

/**
 *
 */
public class SimpleTest {

    //vardef test String
    /**
     *
     */
   private String[] test1=new String[]{"vardef vardef1 int x 1", "quit"};
    /**
     *
      */
    private String[] test2=new String[]{"vardef vardef1 bool x false", "vardef vardef2 bool y true", "quit"};



    /*Binexpr test String*/

    // + - * / % for int
    /**
     *
      */
    private String[] test3 = new String[]{"vardef vardef1 int x 20", "vardef vardef2 int y 100", "binexpr exp1 x + 3", "binexpr exp2 y - 1", "binexpr exp3 x * 2", "binexpr exp4 y / 3", "binexpr exp5 y % 5", "quit"};
    // != == > < >= <= for int
    /**
     *
      */
    private   String[] test4 = new String[]{"vardef vardef1 int x 20", "vardef vardef2 int y 100", "binexpr exp1 x != 10", "binexpr exp2 x == 10", "binexpr exp3 x > 10", "binexpr exp4 x < 10", "binexpr exp5 y >= 20", "binexpr exp6 y <= 20", "quit"};
    // != == for bool
    /**
     *
      */
    private String[] test5 = new String[]{"vardef vardef1 bool x true", "binexpr exp1 x != false", "binexpr ex2 x == false", "quit"};
    // || && for bool
    /**
     *
      */
    private String[] test6 = new String[]{"vardef vardef1 bool x true", "binexpr exp1 x || false", "binexpr exp1 x && false", "quit"};
    //错误处理
    /**
     *
      */
    private String[] test7 = new String[]{"vardef vardef1 bool x true", "binexpr exp1 x ~ false", "binexpr exp2 x && false", "quit"};
    /**
     *
      */
    private String[] test71 = new String[]{"vardef vardef1 int x 0", "binexpr exp1 4 / x", "binexpr exp2 4 % x", "quit"};
    // expr表达式，不是直接数字或bool
    /**
     *
      */
    private String[] test8 = new String[]{"vardef vardef1 int x 20", "vardef vardef2 int y 100", "binexpr exp1 x + y", "quit"};
    /**
     *
      */
    private   String[] test9 = new String[]{"vardef vardef1 bool x true", "vardef vardef2 bool y true", "binexpr exp1 x != y", "quit"};

    /*Unexpr test String*/

    /**
     *
      */
    private String[] test10 = new String[]{"vardef vardef1 bool x true", "unexpr exp1 ! x", "quit"};
    /**
     *
      */
    private String[] test11 = new String[]{"vardef vardef1 int x -24", "unexpr exp1 # x", "quit"};//好像没取绝对值
    /**
     *
      */
    private String[] test12 = new String[]{"vardef vardef1 int x 56", "unexpr exp1 ~ x", "quit"};
    //错误处理
    /**
     *
      */
    private String[] test13 = new String[]{"vardef vardef1 int x 56", "unexpr exp1 * x", "quit"};

    /*Assign test String*/

    //for vardef
    /**
     *
      */
    private String[] test14 = new String[]{"vardef vardef1 int x 0", "binexpr exp1 x + 99", "assign assign1 x exp1", "quit"};
    //for int exp
    /**
     *
      */
    private String[] test15 = new String[]{"vardef vardef1 int x 20", "vardef vardef2 int y 100", "binexpr exp1 x + 3", "assign assign1 y exp1", "quit"};
    //for bool exp
    /**
     *
      */
    private String[] test16 = new String[]{"vardef vardef1 bool x true", "vardef vardef2 bool y false", "unexpr exp1 ! x", "assign assign1 y exp1", "quit"};
    //print test String
    /**
     *
      */
    private String[] test17 = new String[]{"vardef vardef1 int x 520", "vardef vardef2 bool y false","binexpr exp1 x + 20", "unexpr exp2 ! y","print print1 exp1","print print2 exp2", "quit"};





    /*If test String*/
    // Vardef case
    /**
     *
      */
    private String[] test18 = new String[]{"vardef vardef1 int x 9","binexpr exp1 x + 1","binexpr exp2 x - 1","binexpr exp3 x > 5","assign assign1 x exp1","assign assign2 x exp2","print print1 x","if if1 exp3 assign1 assign2","block block1 vardef1 if1 print1","program program1 block1","execute program1"};
    //assign case
    /**
     *
      */
    private String[] test19 = new String[]{"vardef vardef1 int x 7", "binexpr exp1 x + 1","binexpr exp2 x - 1","binexpr exp3 x > 5","if if1 exp3 assign1 assign2","if if2 exp3 assign2 assign1","block block1 if1 if2","program program1 block1","execute program1"};
    //skip and print case
    /**
     *
      */
    private   String[] test20 = new String[]{"vardef vardef1 int x 7", "binexpr exp1 x + 3", "skip skip1", "print print1 exp1", "assign assign1 x exp1","binexpr exp2 x > 17","binexpr exp3 x < 17","if if1 exp2 skip1 print1","if if2 exp3 skip1 print1", "block block1 vardef1 if1 if2","program program1 block1","execute program1"};
    /**
     *
      */
    private String[] test21 = new String[]{"vardef vardef1 int x 9","binexpr exp1 x + 1","binexpr exp2 x - 1","binexpr exp3 x > 5","assign assign1 x exp1","assign assign2 x exp2","print print1 x","if if1 exp3 print1 assign2","block block1 vardef1 if1 print1","program program1 block1","execute program1"};
    //block case
    /**
     *
      */
    private String[] test22 = new String[]{"vardef vardef1 int x 7", "binexpr exp1 x + 3", "assign assign1 x exp1", "binexpr exp2 x > 14","binexpr exp3 x < 20","block block1 assign1", "if if1 exp2 block1 block2", "if if2 exp3 block1 block2","block block3 if1 if2","program program1 block3","execute pogram1"};
    //if case
    // String[] test23 = new String[]{"vardef vardef1 int x 7", "vardef vardef2 int y 0", "if if1 true vardef1 vardef2", "if if2 false vardef1 vardef2", "if if3 true if1 if2", "if if4 false if1 if2", "block block1 if1 if2 if3 if4","program program1","execute program1"};
    //loop caseunexpr
    /**
     *
      */
    private   String[] test24 = new String[]{"vardef vardef1 int x 7", "vardef vardef2 int y 0", "binexpr exp1 x + 3", "binexpr exp2 y + 2","assign assign1 x exp1","assign assign2 y exp2","binexpr exp3 x < 14","binexpr exp4 y < 5", "while while1 exp3 assign1", "while while2 exp4 assign2","block block1 while1 while2","program program1 block1","execute program1"};


    /*loop test String*/

    //Assign case
    /**
     *
      */
    private String[] test25 = new String[]{"vardef vardef1 int x 7", "vardef vardef2 int y 0", "binexpr exp1 x + 3", "binexpr exp2 y + 1", "binexpr exp3 y <= 6", "assign assign1 y exp2", "while while1 ep3 assign1","block block1 while1","program program1 blcok1","execute program1", "quit"};
    //Block case
    /**
     *
      */
    private String[] test26 = new String[]{"vardef vardef1 int x 7", "vardef vardef2 int y 0", "binexpr exp1 x + 3", "binexpr exp2 y + 1", "binexpr exp3 y <= 6", "assign assign1 x exp1", "assign assign2 y exp2", "block block1 print1 assign1 assign2", "while while1 exp3 block1","block block2 vardef2 while1","program program1 block2","execute program1","quit"};




    //block test string and Program test String and execute test String

    //contain loop block if
    //String[] test27 = new String[]{"vardef vardef1 int x 7", "binexpr exp1 x + 2","assign assign1 x exp1", "skip skip1","binexpr exp2 x > 15","binexpr exp3 x + 5", "assign assign2 x exp3","block block1 vardef1 assign1","if if1 exp2 skip1", "while while1 exp2 assign2 ", "block block2 if1", "quit"};

    //contain vardef assign skip print  and skip test String

    /**
     *
      */
    private   String[] test28= new String[]{"vardef vardef1 int x 7", "binexpr exp1 x % 4", "assign assign1 x exp1", "skip skip1", "print print1 exp1", "block block1 vardef1 exp1 assign1 skip1 print1", "program program1 block1", "execute program1", "quit"};
    //stroe and load and list
    /**
     *
      */
    private String[] test29 = new String[]{"vardef vardef1 int x 7","binexpr exp1 x % 4","assign assign1 x exp1","program program1 vardef1 exp1 assign1","list program1","store program1 d://","load program2 d://program1","list program2","quit"};





    /**
     *
      */
    @Test
    public void testSimpleConstructor(){

        Simple simple = new Simple();

        //testVardef
        assert input(test1);
        assert input(test2);

        //testBinexpr

        assert input(test3);
        assert input(test4);
        assert input(test5);
        assert input(test6);
        assert input(test7);
        assert input(test71);
        assert input(test8);
        assert input(test9);

        //testUnexpr

        assert input(test10);
        assert input(test11);
        assert input(test12);
        assert input(test13);

        //testAssign
        assert input(test14);
        assert input(test15);
        assert input(test16);
        assert input(test17);

        //testIf
        assert input(test18);
        assert input(test19);
        assert input(test20);
        assert input(test21);
        assert input(test22);
        //assert input(test23);
        assert input(test24);


        //testloop

        assert input(test25);
        assert input(test26);

        //test_block_Program_execute

        //assert input(test27);
        assert input(test28);

        assert input(test29);


    }

    /**
     *
     * @param test;
     * @return ;
     */
    public boolean input(String[] test){
        try {
            for (int i = 0; i < test.length; i++) {
                SimpleInterpreter.change(test[i]);
            }
        }catch (Exception e){
            return false;
        }
        return true;
    }
}





