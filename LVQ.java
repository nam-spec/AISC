
import java.util.ArrayList;

class LVQ {

    // Distance calculation
    public int winner(double[][] weights, double[] sample) {
        double D0 = 0;
        double D1 = 0;

        for (int i = 0; i < sample.length; i++) {
            D0 += Math.pow(sample[i] - weights[0][i], 2);
            D1 += Math.pow(sample[i] - weights[1][i], 2);
        }

        // Same condition as your Python version (bug kept intentionally)
        return D0 > D1 ? 0 : 1;
    }

    // Update weights
    public void update(double[][] weights, double[] sample, int J, double alpha, int actual) {
        if (actual == J) {
            // Move closer
            for (int i = 0; i < weights[J].length; i++) {
                weights[J][i] += alpha * (sample[i] - weights[J][i]);
            }
        } else {
            // Move away
            for (int i = 0; i < weights[J].length; i++) {
                weights[J][i] -= alpha * (sample[i] - weights[J][i]);
            }
        }
    }
}

public class Main {

    public static void main(String[] args) {

        // Data
        ArrayList<double[]> X = new ArrayList<>();
        X.add(new double[]{0, 0, 1, 1});
        X.add(new double[]{1, 0, 0, 0});
        X.add(new double[]{0, 0, 0, 1});
        X.add(new double[]{0, 1, 1, 0});
        X.add(new double[]{1, 1, 0, 0});
        X.add(new double[]{1, 1, 1, 0});

        ArrayList<Integer> Y = new ArrayList<>();
        Y.add(0);
        Y.add(1);
        Y.add(0);
        Y.add(1);
        Y.add(1);
        Y.add(1);

        // Initialize weights using pop(0) approach
        double[][] weights = new double[2][];
        weights[0] = X.remove(0);
        weights[1] = X.remove(0);

        Y.remove(0);
        Y.remove(0);

        LVQ lvq = new LVQ();
        double alpha = 0.1;
        int epochs = 3;

        // Training
        for (int e = 0; e < epochs; e++) {
            for (int i = 0; i < X.size(); i++) {
                double[] sample = X.get(i);
                int J = lvq.winner(weights, sample);
                lvq.update(weights, sample, J, alpha, Y.get(i));
            }
        }

        // Test
        double[] T = {0, 0, 1, 0};
        int J = lvq.winner(weights, T);

        System.out.println("Sample T belongs to class: " + J);

        // Print trained weights
        System.out.println("Trained weights:");
        for (int c = 0; c < weights.length; c++) {
            System.out.print("Class " + c + ": ");
            for (double v : weights[c]) {
                System.out.print(v + " ");
            }
            System.out.println();
        }
    }
}


//javac Main.java
//java Main
