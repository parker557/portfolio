import java.util.Scanner;
import java.util.UUID;

// 待办事项类
public class PIMEvent extends PIREntity {
	String descriptions;

	String  startTimes;

	PIMEvent() {

		this.type = "event";
		this.pirId = UUID.randomUUID().toString();
	}

	public String getDescriptions() {
		return descriptions;
	}

	public void setDescriptions(String descriptions) {
		this.descriptions = descriptions;
	}

	public String getStartTimes() {
		return startTimes;
	}

	public void setStartTimes(String startTimes) {
		this.startTimes = startTimes;
	}

	@Override
	public String toString() {
		return "PIMEvent{" +
				"descriptions='" + descriptions + '\'' +
				", startTimes='" + startTimes + '\'' +
				", type='" + type + '\'' +
				", pirId='" + pirId + '\'' +
				'}';
	}

	@Override
	public void createPIR() {
		Scanner sc = new Scanner(System.in);
		System.out.println("Enter descriptions for PIMTodo item:");
		this.descriptions = sc.nextLine();

		System.out.println("Enter startTimes for PIMTodo item:");
		this.startTimes = sc.nextLine();
	}

	@Override
	public void modifyPIR() {

		Scanner sc = new Scanner(System.in);
		System.out.println("Enter descriptions for PIMTodo item:");
		this.descriptions = sc.nextLine();

		System.out.println("Enter startTimes for PIMTodo item:");
		this.startTimes = sc.nextLine();
	}

}

