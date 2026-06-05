import java.io.Serializable;

public abstract class PIREntity implements Serializable {
    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getPirId() {
        return pirId;
    }

    public void setPirId(String pirId) {
        this.pirId = pirId;
    }

    String type;

    String pirId;

    // This is actually already defined by the super class
    // Object, but redefined here as abstract to make sure
    // that derived classes actually implement it
    abstract public String toString();

    abstract public void createPIR();
    abstract public void modifyPIR();

}
