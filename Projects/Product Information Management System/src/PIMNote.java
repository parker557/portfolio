import java.util.Scanner;
import java.util.UUID;

// 备忘类
public class PIMNote extends PIREntity {
	String noteText;


	PIMNote() {
		this.type = "note";
		this.pirId = UUID.randomUUID().toString();
	}

	// 返回Note的文本
	public String getNoteText() {
		return noteText;
	}
	// 设置Note的文本
	public void setNoteText(String noteText) {
		this.noteText = noteText;
	}

	@Override
	public String toString() {
		return "PIMNote{" +
				"noteText='" + noteText + '\'' +
				", type='" + type + '\'' +
				", pirId='" + pirId + '\'' +
				'}';
	}

	@Override
	public void createPIR() {
		Scanner sc = new Scanner(System.in);
		System.out.println("Enter noteText for PIMNote item:");
		this.noteText = sc.nextLine();
	}

	@Override
	public void modifyPIR() {
		Scanner sc = new Scanner(System.in);
		System.out.println("Enter noteText for PIMNote item:");
		this.noteText = sc.nextLine();
	}

}
