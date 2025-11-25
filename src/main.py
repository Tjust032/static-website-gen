from textnode import TextNode, TextType
import time

def main():
    test_node = TextNode("This is some anchor test", TextType.LINK, "https://www.boot.dev")
    print(test_node)
    # Test with smaller number for actual printing
    print("Testing with printing (1000 iterations):")
    start = time.time()
    for i in range(1000):
        print(i)
    end = time.time()
    print(f"Time with printing: {end - start:.4f} seconds\n")

    # Test without printing (much larger number)
    print("Testing without printing (100 million iterations):")
    start = time.time()
    for i in range(1_000_000_000):
        if i % 100_000_000 == 0:
            print("Lapse")
            lapse_time = time.time()
            print(f"Lapsed time so far: {lapse_time - start:.4f} seconds")
        pass
    end = time.time()
    print(f"Time without printing: {end - start:.4f} seconds")
    
if __name__ == "__main__":
    main()