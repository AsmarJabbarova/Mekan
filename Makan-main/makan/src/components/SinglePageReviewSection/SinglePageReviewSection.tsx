import { useEffect, useRef, useState } from 'react';
import './SinglePageReviewStyles.css';
import { FaRegStar, FaStar } from 'react-icons/fa';
import axios from 'axios';
import { useUser } from '../../contexts/UserContext';

interface Review {
  place_id: number;
  user_id: number;
  date: string;
  rating: number;
  comment: string;
}

interface User {
  id: number;
  username: string;
}

interface SinglePageReviewSectionProps {
  place_id: number;
  rating: number;
}

const SinglePageReviewSection: React.FC<SinglePageReviewSectionProps> = ({ place_id, rating }) => {
  const { id: userId, token } = useUser();
  const [reviews, setReviews] = useState<Review[]>([]);
  const [usernames, setUsernames] = useState<{ [key: number]: string }>({});
  const [userRating, setUserRating] = useState(0);
  const [userComment, setUserComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'; 
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`; 
    }
  }, [userComment]);

  const fetchReviews = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/reviews`);
      const reviewsData = response.data.data;
      if (Array.isArray(reviewsData)) {
        const placeReviews = reviewsData.filter((review: Review) => review.place_id === place_id);
        setReviews(placeReviews);

        const userIds = Array.from(new Set(placeReviews.map((review) => review.user_id)));
        const userPromises = userIds.map((id) => axios.get(`${import.meta.env.VITE_API_URL}/users/${id}`));
        const userResponses = await Promise.all(userPromises);

        const users: User[] = userResponses.map((res) => res.data);
        const usernamesMap = users.reduce((acc, user) => {
          acc[user.id] = user.username;
          return acc;
        }, {} as { [key: number]: string });
        setUsernames(usernamesMap);
      } else {
        console.error('Expected reviews data to be an array, but got:', reviewsData);
      }
    } catch (error) {
      console.error('Error fetching reviews or usernames:', error);
    }
  };

  useEffect(() => {
    fetchReviews();
  }, [place_id]);

  const handleReviewSubmit = async () => {
    if (!userRating || !userComment) {
      alert("Please add a rating and comment.");
      return;
    }

    try {
      setIsSubmitting(true);
      await axios.post(
        'http://127.0.0.1:5000/reviews',
        {
          place_id,
          user_id: userId,
          rating: userRating,
          comment: userComment,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setUserRating(0);
      setUserComment('');
      alert("Review submitted successfully!");
      await fetchReviews();
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 500) {
        alert("You must be logged in to submit a review.");
        window.location.href = '/login';
      } else {
        console.error("Error submitting review:", error);
        alert("Failed to submit review. Please try again.");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className='review-main-sec'>
      <p className='reviews-title'>Reviews</p>
      <div className="rating-sec">
        <div className="rating-sec-inner">
          <h2>{rating}</h2>
          <p className="gray-p">/5</p>
        </div>
        <p className="gray-p">{reviews.length} Verified review(s)</p>
      </div>
      <p className='reviews-title'>Comments</p>
      
      {token ? (
        <div className="write-review-sec">
          <p className='add-comment-title'>Rate and Comment</p>
          <div className="write-review-rating">
            {[...Array(5)].map((_, i) => (
              i < userRating ? (
                <FaStar
                  key={i}
                  color="#F7931E"
                  onClick={() => setUserRating(i + 1)}
                  style={{ cursor: 'pointer', fontSize: '35px', marginRight: '5px'}} 
                />
              ) : (
                <FaRegStar
                  key={i}
                  color="gray"
                  onClick={() => setUserRating(i + 1)}
                  style={{ cursor: 'pointer', fontSize: '35px' , marginRight: '5px'}} 
                />
              )
            ))}
          </div>
          <textarea
            ref={textareaRef}
            className="write-review-textarea contact-form-input"
            value={userComment}
            onChange={(e) => setUserComment(e.target.value)}
            placeholder="Write your comment here..."
            style={{
              resize: 'none', 
              overflow: 'hidden',
            }}
          />
          <button
            onClick={handleReviewSubmit}
            disabled={isSubmitting}
            className="submit-button"
          >
            {isSubmitting ? "Submitting..." : "Submit Review"}
          </button>
        </div>
      ) : (
        <p>Please log in to add a review.</p>
      )}

      {reviews.length > 0 && (
        <>
          <div className="review-comments-sec">
            {reviews.map((review, index) => (
              <div key={index} className="review">
                <p className="review-username">{usernames[review.user_id] || `User ${review.user_id}`}</p>
                <p className="review-date gray-p">{review.date}</p>
                <div>
                  {[...Array(5)].map((_, i) => (
                    <FaStar key={i} color={i < review.rating ? '#F7931E' : 'gray'} />
                  ))}
                </div>
                <p className="comment">{review.comment}</p>
                {index < reviews.length - 1 && <hr />}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default SinglePageReviewSection;
