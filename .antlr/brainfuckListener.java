// Generated from c:/Users/venya/Downloads/Telegram Desktop/brainfuck_compiler0/brainfuck_compiler0/brainfuck.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link brainfuckParser}.
 */
public interface brainfuckListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link brainfuckParser#prog}.
	 * @param ctx the parse tree
	 */
	void enterProg(brainfuckParser.ProgContext ctx);
	/**
	 * Exit a parse tree produced by {@link brainfuckParser#prog}.
	 * @param ctx the parse tree
	 */
	void exitProg(brainfuckParser.ProgContext ctx);
	/**
	 * Enter a parse tree produced by {@link brainfuckParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterExpr(brainfuckParser.ExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link brainfuckParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitExpr(brainfuckParser.ExprContext ctx);
}