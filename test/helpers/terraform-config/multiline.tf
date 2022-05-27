/*
 * something
 */

/*
 * something
 */

/*
 * something
 */

/*
 * something
 */

/*
 * something
 */

/*
 * something
 */
locals {
  some_strings = ["foo", "bar", "baz"]

  transform = { for s in local.some_strings : s =>
    {
      name = upper(s)
      tag  = "test"
    }
  }
}
/*
 * something
 */

/*
 * something
 */

/*
 * something
 */

/*
 * something
 */

/*
 * something
 */

/*
 * something
 */
