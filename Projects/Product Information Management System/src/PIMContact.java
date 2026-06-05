import java.util.Scanner;
import java.util.UUID;

// 联系人类
public class PIMContact extends PIREntity {

	String name;
	String address;
	String mobileNumber;

	PIMContact() {
		this.type = "contact";
		this.pirId = UUID.randomUUID().toString();
	}

	@Override
	public String toString() {
		return "PIMContact{" +
				"name='" + name + '\'' +
				", address='" + address + '\'' +
				", mobileNumber='" + mobileNumber + '\'' +
				", type='" + type + '\'' +
				", pirId='" + pirId + '\'' +
				'}';
	}

	@Override
	public void createPIR() {
		Scanner sc = new Scanner(System.in);
		System.out.println("Enter name for contact item:");
		this.name = sc.nextLine();

		System.out.println("Enter address for contact item:");
		this.address = sc.nextLine();

		System.out.println("Enter mobileNumber for contact item:");
		this.mobileNumber = sc.nextLine();
	}

	@Override
	public void modifyPIR() {
		Scanner sc = new Scanner(System.in);
		System.out.println("Enter name for contact item:");
		this.name = sc.nextLine();

		System.out.println("Enter address for contact item:");
		this.address = sc.nextLine();

		System.out.println("Enter mobileNumber for contact item:");
		this.mobileNumber = sc.nextLine();
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getAddress() {
		return address;
	}

	public void setAddress(String address) {
		this.address = address;
	}

	public String getMobileNumber() {
		return mobileNumber;
	}

	public void setMobileNumber(String mobileNumber) {
		this.mobileNumber = mobileNumber;
	}

}

