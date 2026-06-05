import java.util.Scanner;
import java.util.UUID;

// 待办事项类 task
public class PIMTodo extends PIREntity {

	String descriptions;

	String deadlines;

	@Override
	public String toString() {
		return "PIMTodo{" +
				"descriptions='" + descriptions + '\'' +
				", deadlines='" + deadlines + '\'' +
				", type='" + type + '\'' +
				", pirId='" + pirId + '\'' +
				'}';
	}

	@Override
	public void createPIR() {
		Scanner sc = new Scanner(System.in);
		System.out.println("Enter descriptions for PIMTodo item:");
		this.descriptions = sc.nextLine();

		System.out.println("Enter deadlines for PIMTodo item:");
		this.deadlines = sc.nextLine();
	}

	@Override
	public void modifyPIR() {
		Scanner sc = new Scanner(System.in);
		System.out.println("Enter descriptions for PIMTodo item:");
		this.descriptions = sc.nextLine();

		System.out.println("Enter deadlines for PIMTodo item:");
		this.deadlines = sc.nextLine();
	}


	PIMTodo() {
		this.type = "task";
		this.pirId = UUID.randomUUID().toString();
	}
	public String getDescriptions() {
		return descriptions;
	}

	public void setDescriptions(String descriptions) {
		this.descriptions = descriptions;
	}

	public String getDeadlines() {
		return deadlines;
	}

	public void setDeadlines(String deadlines) {
		this.deadlines = deadlines;
	}


}

