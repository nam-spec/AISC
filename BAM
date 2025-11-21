public class BAM {

    // -------------------------------------------------------
    // Sign function: converts values to +1 or -1
    // -------------------------------------------------------
    public static int[] sign(int[] vec) {
        int[] result = new int[vec.length];

        for (int i = 0; i < vec.length; i++) {
            if (vec[i] >= 0)
                result[i] = 1;
            else
                result[i] = -1;
        }
        return result;
    }

    // -------------------------------------------------------
    // Outer product of two vectors
    // -------------------------------------------------------
    public static int[][] outerProduct(int[] X, int[] Y) {
        int rows = X.length;
        int cols = Y.length;

        int[][] result = new int[rows][cols];

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                result[i][j] = X[i] * Y[j];
            }
        }

        return result;
    }

    // -------------------------------------------------------
    // Add two matrices
    // -------------------------------------------------------
    public static int[][] addMatrix(int[][] A, int[][] B) {
        int rows = A.length;
        int cols = A[0].length;

        int[][] result = new int[rows][cols];

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                result[i][j] = A[i][j] + B[i][j];
            }
        }

        return result;
    }

    // -------------------------------------------------------
    // Multiply vector with matrix (X * W)
    // -------------------------------------------------------
    public static int[] vectorMatrixMul(int[] vec, int[][] mat) {
        int cols = mat[0].length;
        int[] result = new int[cols];

        for (int j = 0; j < cols; j++) {
            int sum = 0;
            for (int i = 0; i < vec.length; i++) {
                sum += vec[i] * mat[i][j];
            }
            result[j] = sum;
        }

        return result;
    }

    // -------------------------------------------------------
    // Multiply vector with transpose matrix (Y * Wᵀ)
    // -------------------------------------------------------
    public static int[] vectorMatrixTransposeMul(int[] vec, int[][] mat) {
        int rows = mat.length;
        int[] result = new int[rows];

        for (int i = 0; i < rows; i++) {
            int sum = 0;
            for (int j = 0; j < vec.length; j++) {
                sum += vec[j] * mat[i][j];
            }
            result[i] = sum;
        }

        return result;
    }

    // -------------------------------------------------------
    // BAM Training
    // -------------------------------------------------------
    public static int[][] trainBAM(int[][] Xpatterns, int[][] Ypatterns) {

        int rows = Xpatterns[0].length;
        int cols = Ypatterns[0].length;

        int[][] W = new int[rows][cols];  // start with zeros

        for (int p = 0; p < Xpatterns.length; p++) {
            int[] X = Xpatterns[p];
            int[] Y = Ypatterns[p];

            int[][] op = outerProduct(X, Y);  // compute outer product
            W = addMatrix(W, op);             // add to weight matrix
        }

        return W;
    }

    // -------------------------------------------------------
    // BAM Recall
    // -------------------------------------------------------
    public static void recallBAM(int[][] W, int[] X, int[] Y) {

        if (X != null) {
            // X given → compute Y
            int[] Ynew = vectorMatrixMul(X, W);
            Ynew = sign(Ynew);

            // backward pass
            int[] Xnew = vectorMatrixTransposeMul(Ynew, W);
            Xnew = sign(Xnew);

            System.out.print("Recalled Y: ");
            printVector(Ynew);

            System.out.print("Recalled X: ");
            printVector(Xnew);
        }

        if (Y != null) {
            // Y given → compute X
            int[] Xnew = vectorMatrixTransposeMul(Y, W);
            Xnew = sign(Xnew);

            // forward pass
            int[] Ynew = vectorMatrixMul(Xnew, W);
            Ynew = sign(Ynew);

            System.out.print("Recalled X: ");
            printVector(Xnew);

            System.out.print("Recalled Y: ");
            printVector(Ynew);
        }
    }

    // -------------------------------------------------------
    // Utility: print a vector
    // -------------------------------------------------------
    public static void printVector(int[] vec) {
        System.out.print("[ ");
        for (int x : vec) {
            System.out.print(x + " ");
        }
        System.out.println("]");
    }


    // -------------------------------------------------------
    // MAIN (Just like your lab experiment)
    // -------------------------------------------------------
    public static void main(String[] args) {

        int[][] Xtrain = {
                {1, -1},
                {-1, 1}
        };

        int[][] Ytrain = {
                {1, 1, -1},
                {-1, -1, 1}
        };

        System.out.println("Training BAM...\n");

        int[][] W = trainBAM(Xtrain, Ytrain);

        // Print W
        System.out.println("Weight Matrix W:");
        for (int i = 0; i < W.length; i++) {
            for (int j = 0; j < W[0].length; j++) {
                System.out.print(W[i][j] + " ");
            }
            System.out.println();
        }

        // Recall using X
        int[] Xtest = {1, -1};
        System.out.println("\nGiven X:");
        printVector(Xtest);
        recallBAM(W, Xtest, null);

        // Recall using Y
        int[] Ytest = {1, 1, -1};
        System.out.println("\nGiven Y:");
        printVector(Ytest);
        recallBAM(W, null, Ytest);
    }
}
