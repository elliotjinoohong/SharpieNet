import os
import preprocess
import model_subclassing
import tensorflow as tf


def main():
    # defining hyperparameters
    batch_size = 8
    original_size = 300
    upscale_factor = 3
    input_size = original_size // upscale_factor
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    loss_fn = tf.keras.losses.MeanSquaredError()

    # joining relative path to form a full path
    dirname = os.path.dirname(__file__)
    image_path = os.path.join(dirname, "BSDS500/data/images")

    train_data, test_data = \
        preprocess.get_normalized_data(image_path, batch_size, original_size)

    # Scale from (0, 255) to (0, 1)
    train_data = train_data.map(preprocess.normalize)
    test_data = test_data.map(preprocess.normalize)

    train_data = train_data.map(
        lambda x: (preprocess.process_input(x, input_size), preprocess.process_target(x))
    )

    # prefetch is for computation optimization
    train_data = train_data.prefetch(buffer_size=32)

    test_data = test_data.map(
        lambda x: (preprocess.process_input(x, input_size), preprocess.process_target(x))
    )

    # prefetch is for computation optimization
    test_data = test_data.prefetch(buffer_size=32)

    print("PREPROCESSING IS DONE")

    # initialize the model
    model = model_subclassing.EDSR_super(input_size)
    # train the model using l1 loss
    weights_file = os.path.join(dirname, 'l1_training_weights.h5')
    model.train_l1(train_data, 200, validation_data=test_data, verbose=2)
    model.save_weights(weights_file)
    # train the model using perceptual loss


    # test the model and output results
    # TODO: load and preprocess test_data
    # TODO: call model.predict
    # TODO: post process prediction back into rgb and output image files




if __name__ == "__main__":
    main()
