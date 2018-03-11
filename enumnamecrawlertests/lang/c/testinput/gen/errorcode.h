#ifndef _ERRORCODE_H_
#define _ERRORCODE_H_ 1

#define TESTINPUT_DIVIDEND_NEGATIVE -1
#define TESTINPUT_DIVISOR_NEGATIVE -2
#define TESTINPUT_DIVIDE_BY_ZERO -3

char * errorcode_string(int errorcode);

#endif	/* _ERRORCODE_H_ */
