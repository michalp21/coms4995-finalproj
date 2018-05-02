import java.util.Arrays;
import java.util.Random;
import java.util.TreeMap;

public class KuhnTrainer {
    public static final int PASS = 0, BET = 1, NUM_ACTIONS = 2;
    public static final Random random = new Random();
    public TreeMap<String, Node> nodeMap = new TreeMap<String, Node>();

    //Information set node class definition
    class Node {
        String infoSet;
        double[] regretSum = new double[NUM_ACTIONS],
            strategy = new double[NUM_ACTIONS],
            strategySum = new double[NUM_ACTIONS];

        private double[] getStrategy(double realizationWeight) {
            double normalizingSum = 0;
            for (int a = 0; a < NUM_ACTIONS; a++) {
                strategy[a] = regretSum[a] > 0 ? regretSum[a] : 0;
                normalizingSum += strategy[a];
            }
            for (int a = 0; a < NUM_ACTIONS; a++) {
                if (normalizingSum > 0)
                    strategy[a] /= normalizingSum;
                else
                    strategy[a] = 1.0 / NUM_ACTIONS;
                strategySum[a] += realizationWeight * strategy[a];
            }
            return strategy;
        }

        public double[] getAverageStrategy() {
            double[] avgStrategy = new double[NUM_ACTIONS];
            double normalizingSum = 0;
            for (int a = 0; a < NUM_ACTIONS; a++)
                normalizingSum += strategySum[a];
            for (int a = 0; a < NUM_ACTIONS; a++) {
                if (normalizingSum > 0)
                    avgStrategy[a] = strategySum[a] / normalizingSum;
                else
                    avgStrategy[a] = 1.0 / NUM_ACTIONS;
            }
            return avgStrategy;
        }

        public String toString() {
            return String.format("%4s: %s", infoSet, Arrays.toString(getAverageStrategy()));
        }
    }

    //Train Kuhn Poker
    public void train(int iterations) {
        int[] cards = {1, 2, 3};
        double util = 0;
        for (int i = 0; i < iterations; i++) {
            //Shuffle cards
            for (int c1 = cards.length - 1; c1 > 0; c1--) {
                int c2 = random.nextInt(c1 + 1);
                int tmp = cards[c1];
                cards[c1] = cards[c2];
                cards[c2] = tmp;
            }
            util += cfr(cards, "", 1, 1);
        }
        System.out.println("Average game value: " + util / iterations);
        for (Node n : nodeMap.values())
            System.out.println(n);
    }

    //Counterfactual regret minimization iteration
    private double cfr(int[] cards, String history, double p0, double p1) {
        int plays = history.length();
        int player = plays % 2;
        int opponent = 1 - player;

        //Return payoff for terminal states
        if (plays > 1) {
            boolean terminalPass = history.charAt(plays - 1) == 'p';
            boolean doubleBet = history.substring(plays - 2, plays).equals("bb");
            boolean isPlayerCardHigher = cards[player] > cards[opponent];
            if (terminalPass)
                if (history.equals("pp"))
                    return isPlayerCardHigher ? 1 : -1;
                else
                    return 1;
            else if (doubleBet)
                return isPlayerCardHigher ? 2 : -2;
        }
        String infoSet = cards[player] + history;

        //Get information set node or create it if nonexistant
        Node node = nodeMap.get(infoSet);
        if (node == null) {
            node = new Node();
            node.infoSet = infoSet;
            nodeMap.put(infoSet, node);
        }

        //For each action, recursively call cfr with additional history and probability
        double[] strategy = node.getStrategy(player == 0 ? p0 : p1);
        double[] util = new double[NUM_ACTIONS];
        double nodeUtil = 0;
        for (int a = 0; a < NUM_ACTIONS; a++) {
            String nextHistory = history + (a == 0 ? "p" : "b");
            util[a] = player == 0
                ? - cfr(cards, nextHistory, p0 * strategy[a], p1)
                : - cfr(cards, nextHistory, p0, p1 * strategy[a]);
            nodeUtil += strategy[a] * util[a];
        }

        for (int a = 0; a < NUM_ACTIONS; a++) {
            double regret = util[a] - nodeUtil;
            node.regretSum[a] += (player == 0 ? p1 : p0) * regret;
        }
        
        return nodeUtil;
    }

    public static void main(String[] args) {
        int iterations = 1000000;
        new KuhnTrainer().train(iterations);
    }
    
}
