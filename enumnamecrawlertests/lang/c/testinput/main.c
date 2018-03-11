#include <stdio.h>

#include "errorcode.h"

int positive_divide(int dividend, int divisor) {
	if (dividend < 0) {
		return TESTINPUT_DIVIDEND_NEGATIVE;
	}
	if (divisor < 0) {
		return TESTINPUT_DIVISOR_NEGATIVE;
	}
	if (divisor == 0) {
		return TESTINPUT_DIVIDE_BY_ZERO;
	}
	return (dividend / divisor);
}

int main(int argc, char *argv[]) {
	int quotient;
	quotient = positive_divide(-10, 3);
	if (quotient < 0) {
		printf("ERR: %s.\n", errorcode_string(quotient));
	} else {
		printf("%d = 10 / 3\n", quotient);
	}
	/* Traps: TRAPTESTINPUT_TRAP, TRAP_TESTINPUT_TRAP, TESTINPUTTRAP */
	return 0;
}
