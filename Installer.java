import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.URI;
import java.net.URISyntaxException;

/**
 TODO:
    1. Have it compile the program into a binary
    2. Have it move files to pertinent places
    3. Have it exit
 Capabilities so far:
    1. Gets user to set up their own api key
    2. Sets the API key as an environment variable
 Ideas:
    1. Probably need other Java classes for compiling and what not
    2. Maybe package and ship the installer as a JAR?
    3.Maybe have the installer just install python rather than compiling the python to a binary?
    4. Could this whole thing be programmed in Godot? That would make cross-platform deployment easier
 */

public class Installer extends JFrame{
    private static String key;
    public final String TEXT = "Set Up Your API Key Here";
    public final String URL = "https://aistudio.google.com/app/apikey";
    public Installer(){
        super("Installer Wizard");
        setSize(600, 200);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new FlowLayout());
        JLabel inst = new JLabel("Please follow the instructions here to get an API key, and then click the button below:");
        JLabel link = new JLabel(TEXT);
        link.setForeground(Color.BLUE.darker());
        link.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        link.addMouseListener(new MouseAdapter() {

            @Override
            public void mouseClicked(MouseEvent e) {
                // the user clicks on the label
                try {
                    Desktop.getDesktop().browse(new URI(URL));
                } catch (IOException | URISyntaxException e1) {
                    e1.printStackTrace();
                }
            }

            @Override
            public void mouseEntered(MouseEvent e) {
                // the mouse has entered the label
                link.setText("<html><a href=''>"+TEXT+"</a></html>");
            }

            @Override
            public void mouseExited(MouseEvent e) {
                // the mouse has exited the label
                link.setText(TEXT);
            }
        });

        JButton submit = new JButton("Submit Key");
        submit.addActionListener(e -> {
            try{
                key = JOptionPane.showInputDialog("Enter the key: ");
                if(!key.isEmpty()){
                    setKey(key);
                }else{
                    JOptionPane.showMessageDialog(null, "Invalid key");
                }
            }catch(Exception ex){
                JOptionPane.showMessageDialog(null, "Invalid key");
            }
        });
        add(inst);
        add(link);
        add(submit);
        setVisible(true);
    }
    public void setKey(String key) {
        if (System.getProperty("os.name").toLowerCase().contains("mac") || System.getProperty("os.name").toLowerCase().contains("nux") || System.getProperty("os.name").toLowerCase().contains("aix") || System.getProperty("os.name").toLowerCase().contains("nix")) {
            final String fileName = System.getProperty("user.home") + "/.bashrc";
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName, true))) {
                writer.write("\nexport API_KEY=" + key);
                System.out.println("Text appended successfully to " + fileName);
            } catch (IOException e) {
                System.err.println("An error occurred while appending to the file: " + e.getMessage());
            }
        } else if (System.getProperty("os.name").toLowerCase().contains("win")) {
            //String cmd="setx API_KEY " + key;
            //Runtime.getRuntime().exec(cmd);
            try {
                ProcessBuilder pb = new ProcessBuilder("setx", "API_KEY", key);
                pb.directory(new File(System.getProperty("user.home")));
                Process process = pb.start();

                StringBuilder output = new StringBuilder();
                BufferedReader reader
                        = new BufferedReader(new InputStreamReader(
                        process.getInputStream()));

                String line;
                while ((line = reader.readLine()) != null) {
                    output.append(line);
                    output.append("\n");
                }

                int exitVal = process.waitFor();
                if (exitVal == 0) {
                    System.out.println(
                            "**************************** The Output is ******************************");
                    System.out.println(output);
                    System.exit(0);
                }
            }
            catch (IOException | InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
    public static void main(String[] args){
        new Installer();
    }
}