#include "sf_error.h"

#include <stdarg.h>
#include <stdlib.h>

const char *sf_error_messages[] = {"no error",
                                   "singularity",
                                   "underflow",
                                   "overflow",
                                   "too slow convergence",
                                   "loss of precision",
                                   "no result obtained",
                                   "domain error",
                                   "invalid input argument",
                                   "other error",
                                   NULL};

/* If this isn't volatile clang tries to optimize it away */
static volatile sf_action_t sf_error_actions[] = {
    SF_ERROR_IGNORE, /* SF_ERROR_OK */
    SF_ERROR_IGNORE, /* SF_ERROR_SINGULAR */
    SF_ERROR_IGNORE, /* SF_ERROR_UNDERFLOW */
    SF_ERROR_IGNORE, /* SF_ERROR_OVERFLOW */
    SF_ERROR_IGNORE, /* SF_ERROR_SLOW */
    SF_ERROR_IGNORE, /* SF_ERROR_LOSS */
    SF_ERROR_IGNORE, /* SF_ERROR_NO_RESULT */
    SF_ERROR_IGNORE, /* SF_ERROR_DOMAIN */
    SF_ERROR_IGNORE, /* SF_ERROR_ARG */
    SF_ERROR_IGNORE, /* SF_ERROR_OTHER */
    SF_ERROR_IGNORE  /* SF_ERROR__LAST */
};

void sf_error_set_action(sf_error_t code, sf_action_t action) {
  sf_error_actions[(int)code] = action;
}

sf_action_t sf_error_get_action(sf_error_t code) {
  return sf_error_actions[(int)code];
}

void sf_error(const char *func_name, sf_error_t code, const char *fmt, ...) {
  va_list ap;
  va_start(ap, fmt);
  va_end(ap);
}
