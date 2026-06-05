
import java.util.*;
import java.io.*;

public class PIMManager{

	static String dataFilePath = "PIMDatabase.pim";
	static File dataFile = new File(dataFilePath);
	static LinkedList<PIREntity> itemList = new LinkedList<>();

	public final static List<String> pirTypeList = Arrays.asList("contact","note","task","event");

	private static void loadData() {
		if (dataFile.canRead() && dataFile.length() > 0) { // 可读文件,长度大于0时读取
			try (
					ObjectInputStream ois = new ObjectInputStream(new FileInputStream(dataFile));
			) {
				itemList = (LinkedList<PIREntity>)ois.readObject(); // 将对象反序列化
			} catch(Exception e) {
				e.printStackTrace();
			}
		}
	}

	public static void main(String[] args) throws IOException {

		if (!dataFile.exists()) { // 如果数据文件不存在
			dataFile.createNewFile(); // 新建一个数据文件
		} else loadData(); // 如果数据文件存在,则加载数据


		System.out.println("Welcome to PIM.");
		Scanner sc = new Scanner(System.in);
		String action = "";
		do {

			System.out.println("----------------------PIMManger----------------------");
			System.out.println("Please choose an action:");
			System.out.println("\t\t create");
			System.out.println("\t\t delete");
			System.out.println("\t\t query");
			System.out.println("\t\t modify");
			System.out.println("\t\t export");
			System.out.println("\t\t import");
			System.out.println("\t\t alertDeadlines");
			System.out.println("\t\t alertAlarms");
						System.out.println("\t\t quit");
			System.out.println("-----------------------------------------------------");


			action = sc.nextLine();


			switch (action) {
				case "create":
					createPIR();
					break;
				case "delete":
					deletePIR();
					break;
				case "query":
					queryPIR();
					break;
				case "modify":
					modifyPIR();
					break;
				case "export":
					exportPIR();
					break;
				case "import":
					importPIR();
					break;
				case "quit":
					sc.close();
					break;
				default:
					System.out.println("the command is not exist");
					break;
			}


		} while (!action.equals("quit"));
	}

	private static void importPIR() {

	}
	private static void exportPIR() {
		if (dataFile.canWrite()) { // 可写文件
			try (
					ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(dataFile));
			) {
				oos.writeObject(itemList); // 序列化集合对象
				oos.flush();
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}

	}
	private static void deletePIR()
	{
		System.out.println("Enter the PIR ID that needs to be deleted:");
		Scanner sc = new Scanner(System.in);

		String pirId = sc.nextLine();

		for (int i = 0; i < itemList.size(); i++) {
			PIREntity pirEntity = itemList.get(i);
			if (pirId.equals(pirEntity.getPirId())) {
				itemList.remove(i);
				System.out.println("Deleted Successfully");
				return;
			}
		}

		System.out.println("No corresponding item exists");
	}

	private static void modifyPIR()
	{
		System.out.println("Enter the PIR ID that needs to be modified:");
		Scanner sc = new Scanner(System.in);
		String pirId = sc.nextLine();

        for (PIREntity pirEntity : itemList) {
            if (pirId.equals(pirEntity.getPirId())) {
                pirEntity.modifyPIR();
                System.out.println("Modified Successfully");
            }
        }

		System.out.println("No corresponding item exists");
	}

	private static void printAllPIR()
	{
        for (PIREntity pirEntity : itemList) {
            System.out.println(pirEntity);
        }
	}

	private static void printPIRByTypes()
	{
		System.out.println("----------------------PIMManger----------------------");
		System.out.println("Please choose an item type:");
		System.out.println("\t\t contact");
		System.out.println("\t\t note");
		System.out.println("\t\t task");
		System.out.println("\t\t event");
		System.out.println("-----------------------------------------------------");

		Scanner sc = new Scanner(System.in);
		String type = sc.nextLine();

		switch (type)
		{
			case "contact":
			case "note":
			case "task":
			case "event":
                for (PIREntity pirEntity : itemList) {
                    if (pirEntity.getType().equals(type)) {
                            System.out.println(pirEntity);
                    }
                }
				break;
			default:
				break;
		}

	}

	private static void  printPIRByFields()
	{
		System.out.println("----------------------PIMManger----------------------");
		System.out.println("Please choose an item type:");
		System.out.println("\t\t contact");
		System.out.println("\t\t note");
		System.out.println("\t\t task");
		System.out.println("\t\t event");
		System.out.println("-----------------------------------------------------");

		Scanner sc = new Scanner(System.in);
		String type = sc.nextLine();


		System.out.println("Please input key world:");
		String keyWorld = sc.nextLine();


        for (PIREntity pirEntity : itemList) {
          if (pirEntity.toString().contains(keyWorld)) {
			  System.out.println(pirEntity);
		  }

        }

	}

	private static void queryPIR()
	{
		System.out.println("----------------------PIMManger----------------------");
		System.out.println("Please choose a query criterion:");
		System.out.println("\t\t1. print All ");
		System.out.println("\t\t2. based-types");
		System.out.println("\t\t3. based-fields");
		System.out.println("-----------------------------------------------------");

		Scanner sc = new Scanner(System.in);
		String action = sc.nextLine();


		switch (action) {
			case "1":
				printAllPIR();
				break;
			case "2":
				printPIRByTypes();
				break;
			case "3":
				printPIRByFields();
				break;
			default:
				break;
		}



	}

	/*private static void printPIREntity(String type, String keyWords) {
		for (int i = 0; i < itemList.size(); ++i) {
			PIREntity pirEntity = itemList.get(i);
			if (pirEntity.getType().equals(type)) {
				if (Objects.equals(keyWords, "")) {
					System.out.println(pirEntity);
				}

				else if(!Objects.equals(keyWords, "") && pirEntity.toString().contains(keyWords)) {
					System.out.println(pirEntity);
				}

			}
		}
	}*/

	private static void createPIR()
	{

		System.out.println("----------------------PIMManger----------------------");
		System.out.println("Please choose an item:");
		System.out.println("\t\t contact");
		System.out.println("\t\t note");
		System.out.println("\t\t task");
		System.out.println("\t\t event");
		System.out.println("-----------------------------------------------------");

		Scanner sc = new Scanner(System.in);
		String type = sc.nextLine();

		switch (type) {
			case "contact":
				PIMContact contact = new PIMContact();
				contact.createPIR();
				itemList.add(contact);
				System.out.println("Created Contact Successfully");
				break;
			case "note":
				PIMNote note = new PIMNote();
				note.createPIR();
				itemList.add(note);
				System.out.println("Created Note Successfully");
				break;
			case "task":
				PIMTodo todo = new PIMTodo();
				todo.createPIR();
				itemList.add(todo);
				System.out.println("Created Task Successfully");
				break;
			case "event":
				PIMEvent pimEvent = new PIMEvent();
				pimEvent.createPIR();
				itemList.add(pimEvent);
				System.out.println("Created Event Successfully");
				break;
			default:
				System.out.println("the item type is not exist");
				break;

		}

	}
}