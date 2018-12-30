import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class SuggestionBox {
    private JTextField suggestion;
    private JButton submitSuggestionButton;
    private JButton showReceivedSubmissionsButton;
    private JTextArea suggestion_list;
    private JPanel BoxPanel;

    public SuggestionBox(){
        submitSuggestionButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                SuggestionBoxSQL setSuggestion = new SuggestionBoxSQL(suggestion.getText(),false);
                suggestion.setText("");
            }
        });

        showReceivedSubmissionsButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                suggestion_list.setText(new SuggestionBoxSQL("",true).outputString);
            }
        });
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("SuggestionBox");
        frame.setContentPane(new SuggestionBox().BoxPanel);
        frame.setVisible(true);
    }
}
